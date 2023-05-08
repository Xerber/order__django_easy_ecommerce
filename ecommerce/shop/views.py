from django.shortcuts import render
from .models import Slider, Category, Product


# Create your views here.
def index(request):
  slider = Slider.objects.filter(draft=False).order_by('queue')
  categories = Category.objects.all()
  new_products = Product.objects.filter(product_status='published',new_product=True)
  context ={
    'sliders': slider,
    'categories': categories,
    'new_products': new_products,
  }
  return render(request,'shop/index.html',context)