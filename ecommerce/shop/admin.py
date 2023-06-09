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


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    '''Баннер'''
    list_display = ("title","draft","get_image")
    list_editable = ("draft",)
    readonly_fields = ("get_image",)

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
    inlines = [ProductShotsInline,]
    save_on_top = True

    def get_image(self,obj):
      return(mark_safe(f'<img src={obj.image.url} width="150" height="150"'))
    
    get_image.short_description="Изображение"

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    '''Избранное'''
    list_display = ("product","user","date")
    readonly_fields = ("user","product")


class ContactUsCommentInline(admin.TabularInline):
    '''Комментарии к обратной связи'''
    model = ContactUsComment
    extra = 1


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    '''Обратная связь'''
    list_display = ("first_name","email","phone","subject","status")
    readonly_fields = ("first_name","last_name","email")
    list_editable = ("status",)
    inlines = [ContactUsCommentInline,]


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    '''Email подписчики'''
    list_display = ("email","date")
    readonly_fields = ("email","date")