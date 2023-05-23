from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


app_name = 'service'


urlpatterns = [
    path('', views.service_view, name='service'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)