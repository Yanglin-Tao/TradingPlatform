from django.urls import path
from . import views
from .views import stock_price


urlpatterns = [
    path('price/<str:symbol>/', stock_price, name='stock_price'),
]
