# Generated by Django 5.0.6 on 2024-07-09 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('work', models.CharField(max_length=50)),
                ('salary', models.IntegerField()),
            ],
        ),
    ]
