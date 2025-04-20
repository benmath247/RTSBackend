from django.urls import path
from core.favorite_views import FavoriteStockDeleteView

urlpatterns = [
    path('favorites/delete/<str:stock_symbol>/', FavoriteStockDeleteView.as_view(), name='favorite-delete'),
]