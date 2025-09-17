from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from cart.models import CartItem
from cart.utils import ensure_session_key
from products.models import Product

from django.contrib import messages
from cart.services import send_cart_to_telegram
from cart.services import get_cart_snapshot


class CartAdd(View):
   def post(self, request):

        session_key = ensure_session_key(request)

        product_slug = request.POST.get('product_slug')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, slug=product_slug, is_active=True)
        messages.success(request, f"Товар «{product.name}» добавлен в корзину")


        item, created = CartItem.objects.get_or_create(
            product=product,
            # владельцем строки будет либо user, либо session_key
            user=request.user if request.user.is_authenticated else None,
            session_key=None if request.user.is_authenticated else session_key,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"]) # сохраняем только поле quantity


        if request.POST.get('return_to') == 'product':
            return redirect(product.get_absolute_url())

        return redirect('cart:cart_detail')



class CartChange(View):
    def post(self, request):
        session_key = ensure_session_key(request)
        pk = request.POST.get('cart_item_id')
        str_quantity = request.POST.get('quantity', 0)

        try:
            quantity = int(str_quantity)
        except (ValueError, TypeError):
            quantity = 0

        item = get_object_or_404(CartItem, pk=pk, session_key=session_key)

        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save(update_fields=['quantity'])

        return redirect('cart:cart_detail')


class CartDetail(ListView):
    model = CartItem
    template_name = 'cart/cart_detail.html'
    context_object_name = 'items'


    def get_queryset(self):
        session_key = ensure_session_key(self.request)
        qs =  CartItem.objects.filter(session_key=session_key).select_related('product')
        for item in qs:
            item.subtotal = item.product.price * item.quantity
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        items = context['items']
        context['total_qty'] = sum(item.quantity for item in items)
        context['total_price'] = sum(item.product.price * item.quantity for item in items)
        context['title'] = 'Корзина'
        return context


def checkout_notify(request):
    items, total_price, total_qty = get_cart_snapshot(request)

    buyer = {
        "name": (request.POST.get("name") or "").strip(),
        "phone": (request.POST.get("phone") or "").strip(),
        "comment": (request.POST.get("comment") or "").strip(),
    }

    ok = send_cart_to_telegram(items, total_price, total_qty, buyer=buyer)  # <-- передаем buyer
    if ok:
        messages.success(request, "Заказ отправлен менеджеру в Telegram. Мы скоро свяжемся.")

        session_key = ensure_session_key(request)
        CartItem.objects.filter(session_key=session_key).delete()
    else:
        messages.error(request, "Не удалось отправить заказ. Попробуйте ещё раз или свяжитесь с нами.")



    return redirect("cart:cart_detail")