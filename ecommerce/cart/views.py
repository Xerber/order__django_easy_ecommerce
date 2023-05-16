from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from shop.models import Category



# Create your views here.
def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
      'id': request.GET['id'],
      'title': request.GET['title'],
      'qty': request.GET['qty'],
      'price': request.GET['price'].split(' ')[0],
      'image': request.GET['image'],
      'get_absolute_url': request.GET['get_absolute_url'],
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