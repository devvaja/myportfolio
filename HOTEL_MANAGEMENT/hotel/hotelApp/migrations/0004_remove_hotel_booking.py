# Generated by Django 5.1.1 on 2024-10-01 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelApp', '0003_hotel_details_alter_booking_check_in_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='booking',
        ),
    ]
