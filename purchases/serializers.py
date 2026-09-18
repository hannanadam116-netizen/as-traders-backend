from rest_framework import serializers

from masters.models import Supplier, Product
from .models import PurchaseInvoice, PurchaseInvoiceItem


class PurchaseInvoiceItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.product_name",
        read_only=True
    )

    class Meta:
        model = PurchaseInvoiceItem
        fields = (
            "id",
            "product",
            "product_name",
            "quantity",
            "purchase_price",
            "total",
        )

        read_only_fields = (
            "purchase_price",
            "total",
        )


class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(
        source="supplier.name",
        read_only=True
    )

    items = PurchaseInvoiceItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = PurchaseInvoice
        fields = (
            "id",
            "invoice_number",
            "display_invoice_number",
            "supplier",
            "supplier_name",
            "invoice_date",
            "payment_type",
            "discount",
            "transport_charge",
            "gst_percent",
            "subtotal",
            "gst_amount",
            "grand_total",
            "items",
        )

        read_only_fields = (
            "invoice_number",
            "display_invoice_number",
            "invoice_date",
            "subtotal",
            "gst_amount",
            "grand_total",
        )


class CreatePurchaseInvoiceItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True)
    )

    quantity = serializers.IntegerField(
        min_value=1
    )

    purchase_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )


class CreatePurchaseInvoiceSerializer(serializers.Serializer):
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.filter(is_active=True)
    )

    invoice_date = serializers.DateField(required=False)

    payment_type = serializers.ChoiceField(
        choices=PurchaseInvoice.PAYMENT_CHOICES
    )

    discount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        default=0
    )

    transport_charge = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        default=0
    )

    gst_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        default=0
    )

    items = CreatePurchaseInvoiceItemSerializer(
        many=True
    )