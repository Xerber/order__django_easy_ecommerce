from django.shortcuts import render
from .models import Slider, Category


# Create your views here.
def index(request):
  slider = Slider.objects.filter(draft=False).order_by('queue')
  categories = Category.objects.all()
  context ={
    'sliders': slider,
    'categories': categories,
  }
  return render(request,'shop/index.html',context)