# Generated by Django 5.0.7 on 2024-07-30 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_order'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stock_price',
            new_name='Price',
        ),
        migrations.RenameField(
            model_name='price',
            old_name='timeStamp',
            new_name='time',
        ),
    ]
