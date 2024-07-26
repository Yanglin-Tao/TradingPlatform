from django.urls import path
from . import views
from .views import stock_price


urlpatterns = [
    path('price/<str:symbol>/', stock_price, name='stock_price'),
    path('signup', views.signup, name='signup'),
    # path('signin', views.signin, name='signin'),
    # path('signout', views.signout, name='signout'),
]
