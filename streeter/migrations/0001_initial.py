# Generated by Django 4.0.3 on 2022-05-26 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название города')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название улицы')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streeter.city', verbose_name='Город')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название магазина')),
                ('house', models.CharField(max_length=10, verbose_name='Дом')),
                ('open_time', models.DateTimeField(verbose_name='Время открытия')),
                ('close_time', models.DateTimeField(verbose_name='Время закрытия')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streeter.city', verbose_name='Город')),
                ('street', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='streeter.street', verbose_name='Улица')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
