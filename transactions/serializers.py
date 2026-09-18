from rest_framework import serializers

from masters.models import Customer, Product
from .models import SalesInvoice, SalesInvoiceItem


class SalesInvoiceItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.product_name",
        read_only=True
    )
    hsn_code = serializers.CharField(
      source="product.hsn_code",
      read_only=True,
    )

    class Meta:
        model = SalesInvoiceItem
        fields = (
            "id",
            "product",
            "product_name",
            "hsn_code",
            "quantity",
            "purchase_price",
            "selling_price",
            "gst_percent",
            "gst_amount",
            "total",
            "profit",
        )
        read_only_fields = (
            "purchase_price",
            "selling_price",
            "gst_percent",
            "total",
            "profit",
        )


class SalesInvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source="customer.name",
        read_only=True
    )

    items = SalesInvoiceItemSerializer(many=True)

    class Meta:
        model = SalesInvoice
        fields = (
            "id",
            "invoice_number",
            "display_invoice_number",
            "customer",
            "customer_name",
            "invoice_date",
            "payment_type",
            "discount",
            "transport_charge",
            "gst_percent",
            "subtotal",
            "gst_amount",
            "grand_total",
            "total_profit",
            "items",
        )

        read_only_fields = (
            "invoice_number",
            "display_invoice_number",
            "subtotal",
            "gst_amount",
            "grand_total",
            "total_profit",
            "invoice_date",
        )


class CreateInvoiceItemSerializer(serializers.Serializer):

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True)
    )

    quantity = serializers.IntegerField(
        min_value=1
    )

    selling_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
    )


class CreateInvoiceSerializer(serializers.Serializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.filter(is_active=True)
    )
    invoice_date = serializers.DateField(
      required=False,   
    )

    payment_type = serializers.ChoiceField(
        choices=SalesInvoice.PAYMENT_CHOICES
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

    items = CreateInvoiceItemSerializer(
        many=True
    )