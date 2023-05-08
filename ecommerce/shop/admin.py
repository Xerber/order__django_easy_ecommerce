from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


# Register your models here.
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


class SubCategoryInline(admin.TabularInline):
    '''Подкатегории на странице категории'''
    model = Sub_Category
    extra = 1

class ProductShotsInline(admin.TabularInline):
    '''Дополнительные картинки товара'''
    model = ProductShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self,obj):
      return(mark_safe(f'<img src={obj.image.url} width="150" height="100"'))
    
    get_image.short_description="Изображение"

class SpecificationsInline(admin.TabularInline):
    '''Характеристики товара'''
    model = Specifications
    extra = 3

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Категории'''
    inlines = [SubCategoryInline,]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Товары'''
    list_display = ("title","category","total_quantity","product_status","get_image")
    list_editable = ("product_status",)
    list_filter = ("category__name",)
    search_fields = ("title","category__name")
    readonly_fields = ("get_image",)
    inlines = [ProductShotsInline,SpecificationsInline]
    save_on_top = True

    def get_image(self,obj):
      return(mark_safe(f'<img src={obj.image.url} width="150" height="150"'))
    
    get_image.short_description="Изображение"