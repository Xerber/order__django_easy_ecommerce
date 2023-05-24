from django.db import models
from django.urls import reverse
from shop.models import Product


ORDER_STATUS = (
    ("new","Новый"),
    ("in_progress","Комплектуется"),
    ("on_the_way","Доставляется"),
    ("delivered","Доставлено"),
    ("refund","Возврат"),
)

# Create your models here.
class Order(models.Model):
    order_id = models.PositiveBigIntegerField('Номер заказа')
    first_name = models.CharField('Фамилия', max_length=150)
    last_name = models.CharField('Имя', max_length=150)
    address = models.CharField('Адрес', max_length=250)
    add_address = models.CharField('Комментарий', max_length=250, null=True)
    phone = models.CharField('Номер телефона', max_length=100)
    email = models.EmailField('Email', max_length=254)
    total_amount = models.PositiveBigIntegerField('Сумма заказа')
    cart_data = models.JSONField('JSON корзины')
    status = models.CharField('Статус', choices=ORDER_STATUS, max_length=15, default='new')

    class Meta:
      verbose_name = 'Заказ'
      verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.order_id)


ORDERITEM_STATUS = (
    ("packed","Укомплектовано"),
    ("in_queue","В очереди"),
)

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, verbose_name='Номер заказа',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.DO_NOTHING)
    qty = models.PositiveSmallIntegerField('Количество товара')
    price = models.PositiveBigIntegerField('Цена на момент заказа')
    status = models.CharField('Статус', choices=ORDERITEM_STATUS, max_length=15, default='in_queue')

    class Meta:
      verbose_name = 'Товар'
      verbose_name_plural = 'Товары'

    def __str__(self):
        return self.product.title
