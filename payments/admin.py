from django.contrib import admin

from .models import (
    CustomerPayment,
    SupplierPayment,
)


@admin.register(CustomerPayment)
class CustomerPaymentAdmin(admin.ModelAdmin):

    list_display = (
        "display_receipt_number",
        "customer",
        "payment_date",
        "amount",
        "payment_mode",
    )

    search_fields = (
        "receipt_number",
        "customer__name",
    )

    list_filter = (
        "payment_mode",
        "payment_date",
    )

    readonly_fields = (
        "receipt_number",
        "created_at",
    )

    ordering = (
        "-receipt_number",
    )


@admin.register(SupplierPayment)
class SupplierPaymentAdmin(admin.ModelAdmin):

    list_display = (
        "display_receipt_number",
        "supplier",
        "payment_date",
        "amount",
        "payment_mode",
    )

    search_fields = (
        "receipt_number",
        "supplier__name",
    )

    list_filter = (
        "payment_mode",
        "payment_date",
    )

    readonly_fields = (
        "receipt_number",
        "created_at",
    )

    ordering = (
        "-receipt_number",
    )