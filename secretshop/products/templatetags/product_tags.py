from django import template
from django.db.models import Count
from django.template import Template

from products.models import Category

register = template.Library()

@register.inclusion_tag('products/list_categories.html')
def show_categories():
    categories = Category.objects.annotate(total=Count('products')).filter(total__gt=0)
    return {'categories': categories}