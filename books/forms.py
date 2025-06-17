from django import forms
from .models import Book, Genre, Order

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убедитесь, что числовые поля используют правильные виджеты
        self.fields['year'].widget = forms.NumberInput()
        self.fields['retail_price'].widget = forms.NumberInput(attrs={'step': '0.01'})
        self.fields['wholesale_price'].widget = forms.NumberInput(attrs={'step': '0.01'})
        self.fields['stock'].widget = forms.NumberInput()
        self.fields['sold'].widget = forms.NumberInput()

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'quantity']