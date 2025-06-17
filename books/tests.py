# books/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Genre, Order
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from decimal import Decimal


class BackendTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com'
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpassword')

        self.genre = Genre.objects.create(name='Fantasy')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            genre=self.genre,
            year=2023,
            retail_price=500,
            wholesale_price=300,
            stock=10,
            sold=5
        )

    # 3. Тест удаления книги
    def test_book_deletion(self):
        response = self.client.post(reverse('delete_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 0)

    # 4. Тест фильтрации книг
    def test_book_filtering(self):
        response = self.client.get(
            reverse('book_list') + '?q=Test&genre=Fantasy'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    # 5. Тест статистики авторов (ИСПРАВЛЕН)
    def test_author_stats(self):
        response = self.client.get(reverse('author_stats'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1000')  # (500-300)*5=1000
        self.assertContains(response, 'Test Author')

    # 6. Тест стоимости продаж (ИСПРАВЛЕН)
    def test_sales_value(self):
        response = self.client.get(reverse('sales_value'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2500')  # 500*5=2500
        self.assertContains(response, 'Test Book')

    # 7. Тест максимальной наценки
    def test_price_difference(self):
        response = self.client.get(reverse('price_difference'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '200.00')  # 500-300=200

    # 8. Тест создания заказа
    def test_order_creation(self):
        self.book.stock = 0
        self.book.save()
        response = self.client.post(reverse('create_order'), {
            'book': self.book.id,
            'quantity': 10
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)

    # 9. Тест выполнения заказа
    def test_order_completion(self):
        order = Order.objects.create(book=self.book, quantity=5)
        response = self.client.post(reverse('complete_order', args=[order.id]))
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 15)  # 10 + 5
        self.assertEqual(response.status_code, 302)

    # 10. Тест управления жанрами
    def test_genre_management(self):
        # Создание жанра
        response = self.client.post(reverse('manage_genre'), {'name': 'Science Fiction'})
        self.assertEqual(Genre.objects.count(), 2)

        # Удаление жанра
        genre = Genre.objects.get(name='Science Fiction')
        response = self.client.post(reverse('delete_genre', args=[genre.id]))
        self.assertEqual(Genre.objects.count(), 1)