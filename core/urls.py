from django.urls import path, include
from core.user_views import CurrentUserView, LogoutView, CreateUserView, EditUserView, LoginView
from core.stock_views import StockDataView, StockPriceView
# from core.stock_views import (
#     FavoriteStockListView,
#     FavoriteStockCreateView,
#     FavoriteStockDeleteView,
# )


urlpatterns = [
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/create/', CreateUserView.as_view(), name='create_user'),
    path('user/edit/', EditUserView.as_view(), name='edit_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('stock-data/', StockDataView.as_view(), name='stock_data'),
    path('stock-price/', StockPriceView.as_view(), name='stock_data'),
    # path('favorite-stocks/', FavoriteStockListView.as_view(), name='favorite-stock-list'),
    # path('favorite-stocks/create/', FavoriteStockCreateView.as_view(), name='favorite-stock-create'),
    # path('favorite-stocks/<int:pk>/delete/', FavoriteStockDeleteView.as_view(), name='favorite-stock-delete'),
]