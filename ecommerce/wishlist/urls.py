from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


app_name = 'wishlist'


urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('remove_from_wishlist/', views.remove_wishlist, name='remove_from_wishlist'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)