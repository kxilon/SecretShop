from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from unicodedata import category
from django.db.models import Q

from products.models import Product, Category


def index(request):
    return render(request, template_name='products/product_list.html')

class ProductList(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    title = 'Каталог'

    paginate_by = 6


    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('category')
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        return ctx



class ShowProduct(DetailView):
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'  # в часть url, которая называется product_slug нужно передать аргумент из бд, который по стандарту будет равен в данном случае slug, потому что в самом url указан слаг

    def get_object(self, queryset=None):  # но по сути можно просто передать queryset, потому что этот класс сам отбирает по slug_url_kwarg
        return get_object_or_404(
            Product.objects.filter(is_active=True, slug=self.kwargs[self.slug_url_kwarg])
        )



def about(request):
    return render(request, 'products/about.html')

def contact(request):
    return render(request, 'products/contact.html')


class ProductCategory(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    # slug_url_kwarg = 'category_slug'
    allow_empty = False
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.filter(is_active=True, category__slug=self.kwargs['category_slug']).select_related('category')


    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_category'] = get_object_or_404(Category.objects.filter(slug=self.kwargs['category_slug']))
        ctx['title'] = ctx['current_category'].name
        return ctx

