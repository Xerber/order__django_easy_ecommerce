from django.db import models


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