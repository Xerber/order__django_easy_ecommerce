from django.shortcuts import render, redirect
from .models import Slider, Product, Sub_Category


# Create your views here.
def index(request):
  slider = Slider.objects.filter(draft=False).order_by('queue')
  all_products = Product.objects.all()
  context ={
    'sliders': slider,
    'all_products': all_products,
  }
  return render(request,'shop/index.html',context)


def product_details(request,slug):
    product = Product.objects.filter(slug=slug)
    if len(product) == 0:
        return redirect('error404')
    else:
        product = Product.objects.get(slug=slug)
    context = {
      'product': product,
    }
    return render(request, 'shop/product_detail.html',context)


def page_not_found(request):
    return render(request, 'error/error404.html')


def product_grid(request):
    all_products = Product.objects.all()
    context = {
      'all_products': all_products,
    }
    return render(request, 'shop/product_grid.html',context)


def category_grid(request,url):
    sub_cat = Sub_Category.objects.get(url=url)
    all_products = Product.objects.filter(category=sub_cat)
    context = {
      'all_products': all_products,
    }
    return render(request, 'shop/product_grid.html',context)

def contact_view(request):
    return render(request, 'shop/contact.html')


def search_view(request):
    query = request.GET.get('q')
    all_products = Product.objects.filter(title__icontains=query).order_by("-price") 
    context = {
      'query': query,
      'all_products': all_products
    }
    return render(request, 'shop/product_grid.html',context)
