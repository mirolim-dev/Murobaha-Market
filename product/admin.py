from django.contrib import admin
from .models import Category, Product, ProductImage
from django.utils.html import format_html

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_trending')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'main_image_display')
    search_fields = ('name',)
    list_filter = ('category',)
    inlines = [ProductImageInline]
    readonly_fields = ('get_product_images',)

    def main_image_display(self, obj):
        main_image_url = obj.get_main_image()
        if main_image_url:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" width="50" height="50" /></a>',
                main_image_url
            )
        return "-"
    main_image_display.short_description = 'Main Image'
