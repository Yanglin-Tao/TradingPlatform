# Generated by Django 5.0.7 on 2024-07-30 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_stock_price_price_rename_timestamp_price_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='price',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
