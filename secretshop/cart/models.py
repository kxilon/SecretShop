from dataclasses import fields

from django.conf import settings
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.db.models import CASCADE


class CartItem(models.Model):
    product = models.ForeignKey('products.Product', on_delete=CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=CASCADE)
    session_key = models.CharField(null=True, blank=True, max_length=40)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session_key', 'product'],
                name='unique_session_product',
                condition=models.Q(session_key__isnull=False)
            )
        ]


    def __str__(self):
        return f"{self.session_key}: {self.product.slug} x {self.quantity}"