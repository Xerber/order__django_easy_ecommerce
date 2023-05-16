"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from .views import *
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


app_name = 'cart'


urlpatterns = [
    path('', cart_view, name='cart'),
    path('add-to-cart/', add_to_cart, name="add-to-cart"),
    path('delete-from-cart/', delete_item_from_cart, name="delete-from-cart"),
    path('update-quantity/', update_quantity, name="update-quantity"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)