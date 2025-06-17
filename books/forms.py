from django import forms
from .models import Book, Genre, Order

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'quantity']