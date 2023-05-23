from django.shortcuts import render
from .models import Service



# Create your views here.
def service_view(request):
    all_services = Service.objects.filter(status='published')

    context ={
        'all_services': all_services,
    }

    return render(request, 'service/service.html',context)