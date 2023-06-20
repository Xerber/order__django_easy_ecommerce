from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Category, Sub_Category, Product
from cart.models import Order, OrderItem


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = {
            'id': 0,
            'title': 'test_product',
            'qty': 1,
            'price': 1,
            'image': 'test_image.png',
            'get_absolute_url': '/test_product'}
        self.product1 = {
            'id': 1,
            'title': 'test_product1',
            'qty': 1,
            'price': 1,
            'image': 'test_image1.png',
            'get_absolute_url': '/test_product1'}
        self.order = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'address': 'test_address',
            'add_address': 'test_add_address',
            'phone': '+79591112233',
            'email': 'test@gmail.com',
            'total_amount': float(1),
            'cart_data': "{'1': {'id': '1', 'title': 'test_product', 'qty': '1', 'price': '111', 'image': 'test_image.png', 'get_absolute_url': '/shop/product/test_product'}}"}

    def test_cart_view(self):
        response = self.client.get(reverse('cart:cart'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')

    def test_checkout_view(self):
        response = self.client.get(reverse('cart:checkout'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/checkout.html')

    def test_update_quantity(self):
        response = self.client.get(reverse('cart:update-quantity'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/async/cart-list.html')

    def test_add_to_cart_firstitem(self):
        response = self.client.get(reverse('cart:add-to-cart'),self.product)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('cart_data_obj' in self.client.session)
        self.assertEquals(self.client.session['cart_data_obj']['0']['title'], 'test_product')

    def test_add_to_cart_seconditem(self):
        response = self.client.get(reverse('cart:add-to-cart'),self.product)
        response = self.client.get(reverse('cart:add-to-cart'),self.product1)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.client.session['cart_data_obj']), 2)

    def test_add_to_cart_sameitem(self):
        response = self.client.get(reverse('cart:add-to-cart'),self.product)
        response = self.client.get(reverse('cart:add-to-cart'),self.product)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.client.session['cart_data_obj']), 1)
        self.assertEquals(self.client.session['cart_data_obj']['0']['qty'], 2)

    def test_delete_item_from_cart(self):
        self.client.get(reverse('cart:add-to-cart'),self.product)
        self.assertEquals(len(self.client.session['cart_data_obj']), 1)
        response = self.client.get(reverse('cart:delete-from-cart'),self.product)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.client.session['cart_data_obj']), 0)

    def test_delete_missingitem_from_cart(self):
        self.client.get(reverse('cart:add-to-cart'),self.product)
        self.assertEquals(len(self.client.session['cart_data_obj']), 1)
        response = self.client.get(reverse('cart:delete-from-cart'),self.product1)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.client.session['cart_data_obj']), 1)

    def test_update_quantity(self):
        self.client.get(reverse('cart:add-to-cart'),self.product)
        self.assertEquals(len(self.client.session['cart_data_obj']), 1)
        response = self.client.get(reverse('cart:update-quantity'),{'id':0, 'quantity':5})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.client.session['cart_data_obj']['0']['qty'], '5')

    def test_update_missingitem_quantity(self):
        self.client.get(reverse('cart:add-to-cart'),self.product)
        self.assertEquals(len(self.client.session['cart_data_obj']), 1)
        response = self.client.get(reverse('cart:update-quantity'),{'id':1, 'quantity':5})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.client.session['cart_data_obj']['0']['qty'], '1')

    def test_ajax_checkout(self):
        self.client.get(reverse('cart:add-to-cart'),self.product)
        self.assertEquals(len(self.client.session['cart_data_obj']), 1)

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

        response = self.client.get(reverse('cart:ajax_checkout-form'),self.order)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Order.objects.get(order_id=1).first_name, 'test_first_name')
        self.assertEquals(OrderItem.objects.get(order_id=1).product.title, 'test_product')
        self.assertEquals(Product.objects.get(title = 'test_product').total_quantity, 0)

    def test_ajax_checkout_more_exist(self):
        self.client.get(reverse('cart:add-to-cart'),self.product)
        self.assertEquals(len(self.client.session['cart_data_obj']), 1)

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

        response = self.client.get(reverse('cart:ajax_checkout-form'),{
            'first_name': 'test_first_nam',
            'last_name': 'test_last_nam',
            'address': 'test_address',
            'add_address': 'test_add_address',
            'phone': '+79591112233',
            'email': 'test@gmail.com',
            'total_amount': float(5),
            'cart_data': "{'1': {'id': '1', 'title': 'test_product', 'qty': '5', 'price': '111', 'image': 'test_image.png', 'get_absolute_url': '/shop/product/test_product'}}"
        })
        self.assertEquals(response.status_code, 200)
        self.assertIsNone(Order.objects.first())
        self.assertIsNone(OrderItem.objects.first())
        self.assertEquals(Product.objects.get(title = 'test_product').total_quantity, 1)

    def test_ajax_checkout_missing_item(self):
        self.client.get(reverse('cart:add-to-cart'),self.product)
        self.assertEquals(len(self.client.session['cart_data_obj']), 1)

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

        response = self.client.get(reverse('cart:ajax_checkout-form'),{
            'first_name': 'test_first_nam',
            'last_name': 'test_last_nam',
            'address': 'test_address',
            'add_address': 'test_add_address',
            'phone': '+79591112233',
            'email': 'test@gmail.com',
            'total_amount': float(1),
            'cart_data': "{'3': {'id': '1', 'title': 'test_product', 'qty': '1', 'price': '111', 'image': 'test_image.png', 'get_absolute_url': '/shop/product/test_product'}}"
        })
        self.assertEquals(response.status_code, 200)
        self.assertIsNone(Order.objects.first())
        self.assertIsNone(OrderItem.objects.first())