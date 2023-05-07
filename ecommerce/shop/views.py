from django.shortcuts import render
from .models import Slider


# Create your views here.
def index(request):
  slider = Slider.objects.filter(draft=False).order_by('queue')
  context ={
    'sliders': slider,
  }
  return render(request,'shop/index.html',context)