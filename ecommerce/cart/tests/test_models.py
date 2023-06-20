from django.test import TestCase
from shop.models import Category, Sub_Category, Product
from cart.models import Order, OrderItem



class TestViews(TestCase):

    def setUp(self):
        Category.objects.create(
            name = 'test_category',
            url = 'test_category_url'
        )
        self.assertTrue(Category.objects.get(name = 'test_category'))

        Sub_Category.objects.create(
            category = Category.objects.get(name = 'test_category'),
            name = 'test_subcategory',
            url = 'test_subcategory_url'
        )
        self.assertTrue(Sub_Category.objects.get(name = 'test_subcategory'))

        Product.objects.create(
            title = 'test_product',
            slug = 'test_product',
            category = Sub_Category.objects.get(name = 'test_subcategory'),
            total_quantity = 1,
            description = 'test_description',
            specifications = 'test_specifications',
            image = 'test_image.png',
            price = 111,
            past_price = 11,
            tag = 'test',
            new_product = False,
            product_status = 'published'
        )
        self.assertTrue(Product.objects.get(title = 'test_product'))

        self.add_order = Order.objects.create(
            order_id = 1,
            first_name = 'test_first_name',
            last_name = 'last_name',
            address = 'address',
            add_address = 'add_address',
            phone = '+79591112233',
            email = 'test@gmail.com',
            total_amount = 111,
            cart_data = "{'1': {'id': '1', 'title': 'test_product', 'qty': '1', 'price': '111', 'image': 'test_image.png', 'get_absolute_url': '/shop/product/test_product'}}",
            status = 'new'
        )
    
    def test_order_add(self):
        self.add_order
        self.assertEquals(len(Order.objects.all()),1)

    def test_orderitem_add(self):
        self.add_order
        OrderItem.objects.create(
            order_id = Order.objects.first(),
            product = Product.objects.first(),
            qty = 1,
            price = 1,
            status = 'in_queue'
        )
        self.assertEquals(len(OrderItem.objects.all()),1)
