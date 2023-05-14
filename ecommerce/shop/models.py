from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField


# Create your models here.
class Slider(models.Model):
    '''Слайдер'''
    image = models.ImageField('Изображение', upload_to='slider', default='base/slider.jpg')
    title = models.CharField('Заголовок', max_length=100)
    body = models.CharField('Текст под заголовком', max_length=100)
    link = models.CharField('Ссылка', max_length=200)
    button_name = models.CharField('Название кнопки', max_length=100)
    queue = models.PositiveSmallIntegerField('Очередь')
    draft = models.BooleanField('Черновик', default=True)

    class Meta:
      verbose_name = 'Слайдер'
      verbose_name_plural = 'Слайды'
      
    def __str__(self):
        return self.title



class Category(models.Model):
    '''Категория'''
    name = models.CharField('Название', max_length=100)
    url = models.SlugField(max_length=160)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Sub_Category(models.Model):
    '''Подкатегория'''
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=100)
    url = models.SlugField(max_length=160)

    def get_absolute_url(self):
        return reverse('shop:category_grid', kwargs={'url': self.url})

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f'{self.category} | {self.name}'


STATUS = (
    ("draft","Черновик"),
    ("disabled","Скрыто"),
    ("published","Опубликовано"),
)


class Product(models.Model):
    '''Товар'''
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField(max_length=160)
    category = models.ForeignKey(Sub_Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    total_quantity = models.PositiveSmallIntegerField('Общее количество')
    description = RichTextField('Описание')
    specifications = RichTextField('Характеристики')
    image = models.ImageField('Изображение', upload_to='product', default='base/Product.jpg')
    price = models.IntegerField('Цена')
    past_price = models.IntegerField('Цена до скидки', blank=True, null=True)
    tag = models.CharField('Тэг', max_length=25, blank=True, null=True)
    new_product = models.BooleanField('Новинка', default=False)
    product_status = models.CharField('Статус', choices=STATUS, max_length=10, default='draft')

    class Meta:
      verbose_name = 'Товар'
      verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

class ProductShots(models.Model):
    '''Доп. картинки товара'''
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    image = models.ImageField('Изображение', upload_to = 'ProductShot')
    
    class Meta:
      verbose_name = 'Доп. картинка товара'
      verbose_name_plural = 'Доп. картинки товара'
