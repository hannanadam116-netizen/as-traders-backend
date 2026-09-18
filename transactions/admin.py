from django.contrib import admin
from .models import SalesInvoice, SalesInvoiceItem


class SalesInvoiceItemInline(admin.TabularInline):
    model = SalesInvoiceItem
    extra = 1


@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "display_invoice_number",
        "customer",
        "invoice_date",
        "payment_type",
        "subtotal",
        "gst_amount",
        "grand_total",
        "total_profit",
    )

    list_filter = (
        "payment_type",
        "invoice_date",
    )

    search_fields = (
        "invoice_number",
        "customer__name",
    )

    readonly_fields = (
        "invoice_number",
        "subtotal",
        "gst_amount",
        "grand_total",
        "total_profit",
        "created_at",
    )

    inlines = [SalesInvoiceItemInline]


@admin.register(SalesInvoiceItem)
class SalesInvoiceItemAdmin(admin.ModelAdmin):
    list_display = (
        "invoice",
        "product",
        "quantity",
        "purchase_price",
        "selling_price",
        "total",
        "profit",
    )

    search_fields = (
        "invoice__invoice_number",
        "product__product_name",
    )

    list_filter = (
        "product",
    )