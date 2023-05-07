from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


# Register your models here.
#admin.site.register(Slider)
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    '''Слайдеры'''
    list_display = ("title","body","button_name","draft","get_image")
    list_editable = ("draft",)
    readonly_fields = ("get_image",)
    save_on_top = True

    def get_image(self,obj):
      return(mark_safe(f'<img src={obj.image.url} width="150" height="50"'))
    
    get_image.short_description="Изображение"