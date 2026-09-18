from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):

    today_sales = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    today_purchases = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    today_collections = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    today_supplier_payments = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    customer_outstanding = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    supplier_outstanding = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_products = serializers.IntegerField()

    stock_value = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )