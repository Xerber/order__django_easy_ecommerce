from django.shortcuts import render, redirect
from .models import Slider, Category, Product, Sub_Category


# Create your views here.
def index(request):
  slider = Slider.objects.filter(draft=False).order_by('queue')
  categories = Category.objects.all()
  all_products = Product.objects.all()
  context ={
    'sliders': slider,
    'categories': categories,
    'all_products': all_products,
  }
  return render(request,'shop/index.html',context)


def product_details(request,slug):
    product = Product.objects.filter(slug=slug)
    if len(product) == 0:
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


def product_grid(request):
    categories = Category.objects.all()
    all_products = Product.objects.all()
    context = {
      'categories': categories,
      'all_products': all_products,
    }
    return render(request, 'shop/product_grid.html',context)


def category_grid(request,url):
    categories = Category.objects.all()
    sub_cat = Sub_Category.objects.get(url=url)
    all_products = Product.objects.filter(category=sub_cat)
    context = {
      'categories': categories,
      'all_products': all_products,
    }
    return render(request, 'shop/product_grid.html',context)

def contact_view(request):
    categories = Category.objects.all()
    context = {
      'categories': categories,
    }
    return render(request, 'shop/contact.html', context)


def search_view(request):
    categories = Category.objects.all()
    query = request.GET.get('q')
    all_products = Product.objects.filter(title__icontains=query).order_by("-price") 
    context = {
      'categories': categories,
      'query': query,
      'all_products': all_products
    }
    return render(request, 'shop/product_grid.html',context)
