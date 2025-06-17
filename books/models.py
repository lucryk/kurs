from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")

    def __str__(self):
        return self.name

class Book(models.Model):
    MEDIUM_CHOICES = [
        ('P', 'Бумажная'),
        ('E', 'Электронная'),
        ('A', 'Аудио'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=100, verbose_name="Автор")
    code = models.CharField(max_length=50, unique=True, verbose_name="Шифр произведения")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Жанр")
    year = models.PositiveIntegerField(verbose_name="Год издания")
    pages = models.PositiveIntegerField(verbose_name="Количество страниц", blank=True, null=True)
    medium = models.CharField(max_length=1, choices=MEDIUM_CHOICES, verbose_name="Носитель")
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Оптовая цена")
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Розничная цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="В наличии")
    sold = models.PositiveIntegerField(default=0, verbose_name="Продано")

    @property
    def price_difference(self):
        return self.retail_price - self.wholesale_price

    def __str__(self):
        return f"{self.title} ({self.author})"

class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    completed = models.BooleanField(default=False, verbose_name="Выполнен")

    def __str__(self):
        return f"Заказ #{self.id} - {self.book.title}"