# Generated by Django 5.1.1 on 2024-10-07 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelApp', '0012_book_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='number',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='book',
            name='rooms',
            field=models.IntegerField(default=1),
        ),
    ]
