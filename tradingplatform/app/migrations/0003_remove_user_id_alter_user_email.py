# Generated by Django 5.0.7 on 2024-07-26 19:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_stock_price_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="id",
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
