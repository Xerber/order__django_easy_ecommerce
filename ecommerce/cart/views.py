from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core import serializers
from shop.models import Category, Product
from cart.models import Order, OrderItem
import json

# Create your views here.
def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
      'id': request.GET.get('id'),
      'title': request.GET.get('title'),
      'qty': request.GET.get('qty'),
      'price': request.GET.get('price').split(' ')[0],
      'image': request.GET.get('image'),
      'get_absolute_url': request.GET.get('get_absolute_url'),
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_data[str(request.GET['id'])]['qty'])+int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
            
    else:
        request.session['cart_data_obj'] = cart_product
    
        
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


def cart_view(request):
    context = {}
    categories = Category.objects.all()
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            context['cart_data'] = request.session['cart_data_obj']
            context['totalcartitems'] = len(request.session['cart_data_obj'])
    else:
        context['cart_data'] = ''
        context['totalcartitems'] = 0
    context['cart_total_amount'] = cart_total_amount
    context['categories'] = categories

    return render(request, 'cart/cart.html', context)


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("cart/async/cart-list.html", {'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({'data': context, 'totalcartitems': len(request.session['cart_data_obj'])})


def update_quantity(request):
    context = {}

    product_id = request.GET['id']
    quantity = str(request.GET['quantity'])

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(product_id)]['qty'] = str(quantity)
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("cart/async/cart-list.html", {'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({'data': context, 'totalcartitems': len(request.session['cart_data_obj'])})


def checkout_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    else:
        request.session['cart_data_obj'] = ''
    return render(request, 'cart/checkout.html', {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})


def ajax_checkout(request):
    first_name = request.GET['first_name']
    last_name = request.GET['last_name']
    address = request.GET['address']
    add_address = request.GET['add_address']
    phone = request.GET['phone']
    email = request.GET['email']
    total_amount = float(request.GET['total_amount'].replace(',','.'))
    cart_data = request.GET['cart_data']

    last_order = Order.objects.last()
    if last_order:
        new_order_id = last_order.id+1
    else:
        new_order_id = 1

    order = Order(
        order_id=new_order_id,
        first_name=first_name,
        last_name=last_name,
        address=address,
        add_address=add_address,
        phone=phone,
        email=email,
        total_amount=total_amount,
        cart_data=cart_data
        )
    order.save()
    
    try:
    
        new_order = Order.objects.filter(phone=phone).last()

        for product_id, item in json.loads(cart_data.replace("\'","\"")).items():
            if not Product.objects.filter(id = product_id).exists():
                raise Exception('Product DoesNotExist')
            qty = item['qty']
            order_item = OrderItem(
                order_id = Order.objects.get(id=new_order.id),
                product = Product.objects.get(id=product_id),
                qty = item['qty'],
                price = item['price']
            )

            prod = Product.objects.get(id=product_id)
            if prod.total_quantity >= int(qty):
                Product.objects.filter(id=product_id).update(total_quantity=prod.total_quantity-int(qty))
                if 'cart_data_obj' in request.session:
                    if product_id in request.session['cart_data_obj']:
                        cart_data = request.session['cart_data_obj']
                        del request.session['cart_data_obj'][product_id]
                        request.session['cart_data_obj'] = cart_data
            else:
                order.delete()
                data = {
                        "bool": False,
                        "reason": 'qty',
                        "message": f"Ошибка при создании заказа. Обратитесь к Администратору"
                        }
                return JsonResponse({"data": data, 'totalcartitems': len(request.session['cart_data_obj'])})

            order_item.save()

    except Exception as e:
        order.delete()
        data = {
                "bool": False,
                "reason": str(e),
                "message": f"Ошибка при создании заказа. Обратитесь к Администратору"
                }
        return JsonResponse({"data": data, 'totalcartitems': len(request.session['cart_data_obj'])})

    data = {
    "bool": True,
    "message": f"Заказ успешно создан. Номер заказа: {new_order.id}"
    }

    return JsonResponse({"data": data, 'totalcartitems': 0})