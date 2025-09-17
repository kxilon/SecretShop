from cart.models import CartItem
from cart.utils import ensure_session_key
import requests
from django.conf import settings

def send_cart_to_telegram(items, total_price, total_qty, buyer=None):
    if total_qty == 0:
        return False

    lines = ["🛒 Новый заказ (MVP)"]

    if buyer:
        if buyer.get("name"):
            lines.append(f"Имя: {buyer['name']}")
        if buyer.get("phone"):
            lines.append(f"Телефон: {buyer['phone']}")
        if buyer.get("comment"):
            lines.append(f"Комментарий: {buyer['comment']}")
        lines.append("")  # пустая строка перед составом

    lines.append(f"Позиции: {total_qty}")
    lines.append("")
    lines.append("Состав:")
    for it in items:
        lines.append(f"- {it.product.name} ×{it.quantity} · {it.product.price} ₽")

    lines.append("")
    lines.append(f"Итого: {total_price} ₽")

    text = "\n".join(lines)
    url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"
    resp = requests.post(url, data={"chat_id": settings.TG_CHAT_ID, "text": text}, timeout=10)
    return resp.ok

def get_cart_snapshot(request):
    session_key = ensure_session_key(request)
    items = CartItem.objects.filter(session_key=session_key).select_related('product')

    for item in items:
        item.subtotal = item.product.price * item.quantity

    total_price = sum(item.subtotal for item in items)
    total_qty = sum(item.quantity for item in items)
    return items, total_price, total_qty