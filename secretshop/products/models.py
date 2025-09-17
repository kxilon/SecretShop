from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование товара")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Описание товара")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория", related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    is_active = models.BooleanField(default=True, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время редактирования")
    image = models.ImageField(upload_to="products/%Y/%m/", blank=True, null=True, verbose_name="Фото")
    # brand
    # attributes
    # old_price / discount_price


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']


    def get_absolute_url(self):
        return reverse('products:product', kwargs={'product_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


    def get_absolute_url(self):
        return reverse('products:categories', kwargs={'category_slug': self.slug})
