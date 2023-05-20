# Generated by Django 4.2.1 on 2023-05-20 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0007_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('last_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=100, verbose_name='Номер телефона')),
                ('subject', models.CharField(max_length=200, verbose_name='Тема письма')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('in_progress', 'В работе'), ('closed', 'Закрыта')], default='new', max_length=15, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(default='base/banner.jpg', upload_to='banner', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
        migrations.CreateModel(
            name='ContactUsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.contactus', verbose_name='Заявка')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
