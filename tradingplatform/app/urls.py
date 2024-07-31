from django.urls import path
from . import views
from .views import stock_price


urlpatterns = [
    path('price/<str:symbol>/', stock_price, name='stock_price'),
    path('login/', views.login, name='login'),  
    path('signup/',views.signup, name='signup'),
    path('deleteaccount/', views.delete_account, name='delete_account'),
    path('userprofile/', views.get_user_profile, name='user_profile'),
    path('buy/', views.buy, name='buy_stock'),
    path('sell/', views.sell, name='sell_stock'),
    path('history/', views.get_order_history,name='history')
]
