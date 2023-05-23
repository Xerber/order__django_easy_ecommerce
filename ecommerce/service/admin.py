from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Service


# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    '''Услуги'''
    list_display = ("title","status","get_image")
    list_editable = ("status",)
    readonly_fields = ("get_image",)

    def get_image(self,obj):
      return(mark_safe(f'<img src={obj.image.url} width="150" height="150"'))
    
    get_image.short_description="Изображение"