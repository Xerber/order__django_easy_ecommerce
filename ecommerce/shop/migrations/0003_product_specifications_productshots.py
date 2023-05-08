# Generated by Django 4.2.1 on 2023-05-07 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_category_sub_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('url', models.SlugField(max_length=160)),
                ('total_quantity', models.PositiveSmallIntegerField(verbose_name='Общее количество')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(default='base/Product.jpg', upload_to='product', verbose_name='Изображение')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('past_price', models.IntegerField(blank=True, null=True, verbose_name='Цена до скидки')),
                ('tag', models.CharField(blank=True, max_length=25, null=True, verbose_name='Тэг')),
                ('new_product', models.BooleanField(default=False, verbose_name='Новинка')),
                ('best_seller', models.BooleanField(default=False, verbose_name='Топ продаж')),
                ('product_status', models.CharField(choices=[('draft', 'Черновик'), ('disabled', 'Скрыто'), ('published', 'Опубликовано')], default='draft', max_length=10, verbose_name='Статус')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.sub_category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Specifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('detail', models.CharField(max_length=100, verbose_name='Значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Характеристика товара',
                'verbose_name_plural': 'Характеристики товаров',
            },
        ),
        migrations.CreateModel(
            name='ProductShots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='ProductShot', verbose_name='Изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Доп. картинка товара',
                'verbose_name_plural': 'Доп. картинки товара',
            },
        ),
    ]
