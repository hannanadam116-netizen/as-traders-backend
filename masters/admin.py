from django.contrib import admin
from .models import (
    Category,
    Product,
    Customer,
    Supplier,
    CustomerProductPrice,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        
        "product_name",
        "category",
        "purchase_price",
        "default_selling_price",
        "current_stock",
        "is_active",
    )

    search_fields = (
        
        "product_name",
    )

    list_filter = (
        "category",
        "is_active",
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "mobile",
        "city",
        "opening_balance",
        "credit_limit",
        "is_active",
    )

    search_fields = (
        "name",
        "mobile",
        "gst_number",
    )

    list_filter = (
        "city",
        "is_active",
    )

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "mobile",
        "city",
        "opening_balance",
        "is_active",
    )

    search_fields = (
        "name",
        "mobile",
        "gst_number",
    )

    list_filter = (
        "city",
        "is_active",
    )

@admin.register(CustomerProductPrice)
class CustomerProductPriceAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "product",
        "selling_price",
    )

    search_fields = (
        "customer__name",
        "product__product_name",
    )

    list_filter = (
        "customer",
    )