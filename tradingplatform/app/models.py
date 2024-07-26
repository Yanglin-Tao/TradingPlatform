from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)

class Stock_price(models.Model):
    price = models.IntegerField()
    symbol = models.CharField(max_length=30)
    timeStamp = models.DateField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    price = models.ForeignKey(Stock_price, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=30)
    order_operation = models.CharField(max_length=30)
    quantity = models.IntegerField()
    order_time = models.DateField()
    stop_price = models.IntegerField()
    limit_price = models.IntegerField()