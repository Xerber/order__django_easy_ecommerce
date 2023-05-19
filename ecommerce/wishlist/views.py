from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core import serializers
from django.http import JsonResponse
from shop.models import Product, Wishlist


# Create your views here.
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context = {}

    wishlist_count = Wishlist.objects.filter(product=product, user = request.user).count()

    if wishlist_count > 0:
        context = {
          'success': True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product = product,
            user = request.user
        )
        context = {
          'success': True
        }

    return JsonResponse(context)

@login_required
def wishlist_view(request):
    return render(request, 'wishlist/wishlist.html')


def remove_wishlist(request):
    product_id = request.GET['id']
    wishlist = Wishlist.objects.filter(user = request.user)

    product = Wishlist.objects.get(id=product_id)
    product.delete()

    context = {
      'success': True,
      'w': wishlist,
    }
    wishlist_json = serializers.serialize('json',wishlist)
    data = render_to_string("wishlist/async/wishlist-list.html", context)
    return JsonResponse({'data': data, 'w': wishlist_json})