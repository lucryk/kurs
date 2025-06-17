from django.contrib import admin
from .models import Genre, Book, Order

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'retail_price', 'stock')
    list_filter = ('genre', 'medium')
    search_fields = ('title', 'author', 'code')
    readonly_fields = ('price_difference',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'created_at', 'completed')
    list_filter = ('completed',)
    search_fields = ('book__title',)

admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Order, OrderAdmin)