from django.contrib import admin

from products.models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity", "is_active", "created_at")
    list_filter = ("is_active", "category")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ("category",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
