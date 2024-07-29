from django.urls import path
from . import views
from .views import stock_price


urlpatterns = [
    path('price/<str:symbol>/', stock_price, name='stock_price'),
    path('', views.login, name='home'),  
    path('signup/',views.signup,name = 'signup'),
    path('deleteaccount/',views.deleteAccount,name = 'delete_account'),
    path('userprofile/',views.getUserProfile,name = 'user_profile'),
]
