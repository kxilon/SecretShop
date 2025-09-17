from django.contrib import admin

from cart.models import CartItem


class CartItemAdmin(admin.ModelAdmin):
    # что показываем в списке
    list_display = ("product", "quantity", "session_key", "created_at", "updated_at")

    # быстрый поиск
    search_fields = ("session_key", "product__name")

    # оптимизация списка: подтянуть product одним JOIN
    list_select_related = ("product",)

    # сортировка по умолчанию (не обязательно)
    ordering = ("-id",)

admin.site.register(CartItem, CartItemAdmin)