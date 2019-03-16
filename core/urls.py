from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('favorites/', views.my_favorites_view, name='book_favorite')
]