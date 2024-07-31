from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, primary_key=True)
    password = models.CharField()

class Price(models.Model):
    price = models.FloatField()
    symbol = models.CharField(max_length=30)
    time = models.DateTimeField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=30)
    order_operation = models.CharField(max_length=30)
    quantity = models.IntegerField()
    order_time = models.DateTimeField()
    stop_price = models.IntegerField()
    limit_price = models.IntegerField()