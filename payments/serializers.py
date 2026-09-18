from rest_framework import serializers

from masters.models import Customer, Supplier

from .models import (
    CustomerPayment,
    SupplierPayment,
)


# ==========================================================
# CUSTOMER PAYMENT
# ==========================================================

class CustomerPaymentSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="customer.name",
        read_only=True,
    )

    class Meta:
        model = CustomerPayment

        fields = (
            "id",
            "receipt_number",
            "display_receipt_number",
            "customer",
            "customer_name",
            "payment_date",
            "amount",
            "payment_mode",
            "remarks",
        )

        read_only_fields = (
            "receipt_number",
            "display_receipt_number",
            
        )


class CreateCustomerPaymentSerializer(serializers.Serializer):

    payment_date = serializers.DateField()
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.filter(
            is_active=True
        )
    )

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    payment_mode = serializers.ChoiceField(
        choices=CustomerPayment.PAYMENT_MODE
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )


# ==========================================================
# SUPPLIER PAYMENT
# ==========================================================

class SupplierPaymentSerializer(serializers.ModelSerializer):

    supplier_name = serializers.CharField(
        source="supplier.name",
        read_only=True,
    )

    class Meta:
        model = SupplierPayment

        fields = (
            "id",
            "receipt_number",
            "display_receipt_number",
            "supplier",
            "supplier_name",
            "payment_date",
            "amount",
            "payment_mode",
            "remarks",
        )

        read_only_fields = (
            "receipt_number",
            "display_receipt_number",
            
        )


class CreateSupplierPaymentSerializer(serializers.Serializer):
    payment_date = serializers.DateField()
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.filter(
            is_active=True
        )
    )

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    payment_mode = serializers.ChoiceField(
        choices=SupplierPayment.PAYMENT_MODE
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )