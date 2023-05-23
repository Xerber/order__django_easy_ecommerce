from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField



# Create your models here.
STATUS = (
    ("draft","Черновик"),
    ("disabled","Скрыто"),
    ("published","Опубликовано"),
)


class Service(models.Model):
    '''Услуги'''
    title = models.CharField('Заголовок', max_length=200)
    description = RichTextField('Описание')
    image = models.ImageField('Изображение', upload_to='service', default='base/Service.jpg')
    status = models.CharField('Статус', choices=STATUS, max_length=10, default='draft')

    class Meta:
      verbose_name = 'Услуга'
      verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title