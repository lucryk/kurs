from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Genre, Order
from .forms import BookForm, GenreForm, OrderForm
from django.db.models import Sum, F, Max, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models import Q
from decimal import Decimal


def book_list(request):
    # Получаем параметры фильтрации
    genre_filter = request.GET.get('genre', '')
    author_filter = request.GET.get('author', '')
    search_query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    # Базовый запрос с сортировкой
    books = Book.objects.all().order_by('title')

    # Применяем фильтры
    if genre_filter:
        books = books.filter(genre__name__icontains=genre_filter)

    if author_filter:
        books = books.filter(author__icontains=author_filter)

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(genre__name__icontains=search_query)
        )

    # Получаем уникальные значения для фильтров
    genres = Genre.objects.all()
    authors = Book.objects.order_by('author').values_list('author', flat=True).distinct()

    # Пагинация
    paginator = Paginator(books, 10)

    try:
        books_page = paginator.page(page)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)

    # Отладочный вывод
    print(f"Всего книг: {books.count()}")
    if books.exists():
        print(f"Первая книга: {books[0].title}")

    return render(request, 'books/book_list.html', {
        'books_page': books_page,  # Было: 'css': books_page
        'genres': genres,
        'authors': authors,
        'selected_genre': genre_filter,
        'selected_author': author_filter,
        'search_query': search_query
    })


def books_by_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    books = Book.objects.filter(genre=genre).order_by('title')
    return render(request, 'books/book_list.html', {
        'css': books,
        'genre': genre
    })


def books_by_author(request, author):
    books = Book.objects.filter(author__icontains=author).order_by('title')
    return render(request, 'books/book_list.html', {
        'css': books,
        'author': author
    })


def author_stats(request):
    authors = Book.objects.values('author').annotate(
        total_sold=Sum('sold'),
        total_profit=Sum(
            ExpressionWrapper(
                F('sold') * (F('retail_price') - F('wholesale_price')),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    ).filter(total_sold__gt=0).order_by('-total_profit')

    most_profitable = authors.first() if authors else None

    return render(request, 'books/author_stats.html', {
        'most_profitable': most_profitable,
        'authors': authors
    })


def missing_books(request):
    orders = Order.objects.filter(completed=False).select_related('book')
    return render(request, 'books/missing_books.html', {'orders': orders})


def sales_value(request):
    # Рассчитываем общую стоимость с помощью агрегации БД
    total_value = Book.objects.aggregate(
        total=Coalesce(
            ExpressionWrapper(
                Sum(F('sold') * F('retail_price')),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            Decimal('0.00')
        )
    )['total']

    # Получаем книги с продажами через аннотации
    books = Book.objects.filter(sold__gt=0).annotate(
        total_sale_value=ExpressionWrapper(
            F('sold') * F('retail_price'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    ).order_by('-total_sale_value')

    return render(request, 'books/sales_value.html', {
        'total_value': total_value,
        'books': books
    })

def price_difference(request):
    book = Book.objects.annotate(
        diff=ExpressionWrapper(
            F('retail_price') - F('wholesale_price'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    ).order_by('-diff').first()

    if not book:
        messages.info(request, "В базе данных нет книг")
        return redirect('book_list')

    return render(request, 'books/price_difference.html', {'book': book})


def manage_genre(request, genre_id=None):
    # Добавляем список всех жанров для отображения
    genres = Genre.objects.all()

    if genre_id:
        genre = get_object_or_404(Genre, id=genre_id)
        form = GenreForm(request.POST or None, instance=genre)
        success_message = "Жанр успешно обновлен!"
    else:
        genre = None
        form = GenreForm(request.POST or None)
        success_message = "Жанр успешно создан!"

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, success_message)
        return redirect('manage_genre')

    return render(request, 'books/genre_manage.html', {
        'form': form,
        'genres': genres
    })


def delete_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    if request.method == 'POST':
        # Проверяем, есть ли книги с этим жанром
        if Book.objects.filter(genre=genre).exists():
            messages.error(request, "Нельзя удалить жанр, так как с ним связаны книги!")
            return redirect('manage_genre')

        genre.delete()
        messages.success(request, "Жанр успешно удален!")
        return redirect('manage_genre')

    return render(request, 'books/genre_confirm_delete.html', {'genre': genre})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.completed = False

            # Проверяем, есть ли книга в наличии
            if order.book.stock > 0:
                messages.warning(request,
                                 f"Эта книга уже есть в наличии ({order.book.stock} шт.). Заказ не создан.")
                return redirect('missing_books')

            order.save()
            messages.success(request, "Заказ на отсутствующую книгу успешно создан!")
            return redirect('missing_books')
    else:
        form = OrderForm()
        # Фильтруем только книги, которых нет в наличии
        form.fields['book'].queryset = Book.objects.filter(stock=0)

    return render(request, 'books/order_form.html', {'form': form})


@transaction.atomic
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        book = order.book
        book.stock += order.quantity
        book.save()
        order.completed = True
        order.save()
        messages.success(request, f"Заказ выполнен! На склад добавлено {order.quantity} шт. книги '{book.title}'")
        return redirect('missing_books')

    return render(request, 'books/order_confirm.html', {'order': order})


# Добавление книги
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга "{book.title}" успешно добавлена!')
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'books/book_form.html', {
        'form': form,
        'title': 'Добавить книгу'
    })


# Редактирование книги
@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Книга "{book.title}" успешно обновлена!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'books/book_form.html', {
        'form': form,
        'title': 'Редактировать книгу',
        'book': book
    })


# Удаление книги
@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Книга "{book_title}" успешно удалена!')
        return redirect('book_list')

    return render(request, 'books/book_confirm_delete.html', {'book': book})


# Новый функционал: поиск книг
def search_books(request):
    query = request.GET.get('q', '')

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(code__icontains=query)
        ).order_by('title')
    else:
        books = Book.objects.none()

    return render(request, 'books/book_list.html', {
        'css': books,
        'query': query,
        'search_mode': True
    })


# Новый функционал: отчет о прибыли
def profit_report(request):
    # Общая прибыль с явным указанием типа
    total_profit = Book.objects.aggregate(
        total=Coalesce(
            Sum(
                ExpressionWrapper(
                    F('sold') * (F('retail_price') - F('wholesale_price')),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            ), 0.0
        )
    )['total']

    # Прибыль по жанрам
    genres_profit = Genre.objects.annotate(
        total_profit=Coalesce(Sum(F('book__sold') * (F('book__retail_price') - F('book__wholesale_price')), 0.0)
                              ).order_by('-total_profit'))

    # Топ-10 самых прибыльных книг
    top_books = Book.objects.annotate(
        profit=ExpressionWrapper(
            F('sold') * (F('retail_price') - F('wholesale_price')),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    ).filter(profit__gt=0).order_by('-profit')[:10]

    return render(request, 'books/profit_report.html', {
        'total_profit': total_profit,
        'genres_profit': genres_profit,
        'top_books': top_books
    })

