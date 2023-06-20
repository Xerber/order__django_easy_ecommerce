from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cart.views import cart_view, add_to_cart, delete_item_from_cart, update_quantity, checkout_view, ajax_checkout


class TestUrls(SimpleTestCase):
    def test_cart_url_resolved(self):
        url = reverse('cart:cart')
        self.assertEquals(resolve(url).func, cart_view)

    def test_add_url_resolved(self):
        url = reverse('cart:add-to-cart')
        self.assertEquals(resolve(url).func, add_to_cart)

    def test_delete_url_resolved(self):
        url = reverse('cart:delete-from-cart')
        self.assertEquals(resolve(url).func, delete_item_from_cart)

    def test_update_url_resolved(self):
        url = reverse('cart:update-quantity')
        self.assertEquals(resolve(url).func, update_quantity)

    def test_checkout_url_resolved(self):
        url = reverse('cart:checkout')
        self.assertEquals(resolve(url).func, checkout_view)

    def test_ajax_checkout_url_resolved(self):
        url = reverse('cart:ajax_checkout-form')
        self.assertEquals(resolve(url).func, ajax_checkout)