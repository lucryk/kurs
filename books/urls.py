from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('genre/<int:genre_id>/', views.books_by_genre, name='books_by_genre'),
    path('author/<str:author>/', views.books_by_author, name='books_by_author'),
    path('stats/authors/', views.author_stats, name='author_stats'),
    path('missing/', views.missing_books, name='missing_books'),
    path('sales/value/', views.sales_value, name='sales_value'),
    path('price/difference/', views.price_difference, name='price_difference'),
    path('genre/manage/', views.manage_genre, name='manage_genre'),
    path('genre/manage/<int:genre_id>/', views.manage_genre, name='edit_genre'),
    path('genre/delete/<int:genre_id>/', views.delete_genre, name='delete_genre'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/complete/<int:order_id>/', views.complete_order, name='complete_order'),
# Добавим в urlpatterns
path('book/add/', views.add_book, name='add_book'),
path('book/edit/<int:book_id>/', views.edit_book, name='edit_book'),
path('book/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('book/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('search/', views.search_books, name='search_books'),
    path('report/profit/', views.profit_report, name='profit_report'),
]