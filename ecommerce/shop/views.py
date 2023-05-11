from django.shortcuts import render, redirect
from .models import Slider, Category, Product


# Create your views here.
def index(request):
  slider = Slider.objects.filter(draft=False).order_by('queue')
  categories = Category.objects.all()
  all_products = Product.objects.all()
  new_products = Product.objects.filter(product_status='published',new_product=True)
  context ={
    'sliders': slider,
    'categories': categories,
    'new_products': new_products,
    'all_products': all_products,
  }
  return render(request,'shop/index.html',context)


def product_details(request,slug):
    product = Product.objects.filter(slug=slug)
    if len(product) is 0:
        return redirect('error404')
    else:
        product = Product.objects.get(slug=slug)
    categories = Category.objects.all()
    context = {
      'categories': categories,
      'product': product,
    }
    return render(request, 'shop/product_detail.html',context)


def page_not_found(request):
    return render(request, 'error/error404.html')