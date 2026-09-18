from django.contrib import admin

from .models import (
    PurchaseInvoice,
    PurchaseInvoiceItem,
)


class PurchaseInvoiceItemInline(admin.TabularInline):
    model = PurchaseInvoiceItem
    extra = 1


@admin.register(PurchaseInvoice)
class PurchaseInvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "display_invoice_number",
        "supplier",
        "invoice_date",
        "payment_type",
        "grand_total",
    )

    list_filter = (
        "payment_type",
        "invoice_date",
    )

    search_fields = (
        "invoice_number",
        "supplier__name",
    )

    readonly_fields = (
        "invoice_number",
        "subtotal",
        "gst_amount",
        "grand_total",
        "created_at",
    )

    inlines = [
        PurchaseInvoiceItemInline,
    ]


@admin.register(PurchaseInvoiceItem)
class PurchaseInvoiceItemAdmin(admin.ModelAdmin):

    list_display = (
        "invoice",
        "product",
        "quantity",
        "purchase_price",
        "total",
    )

    search_fields = (
        "invoice__invoice_number",
        "product__product_name",
    )