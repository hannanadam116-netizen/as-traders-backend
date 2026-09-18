from rest_framework import serializers


class GSTSummarySerializer(serializers.Serializer):

    sales_taxable = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    sales_gst = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    purchase_taxable = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    purchase_gst = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    gst_payable = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )


class MonthlyGSTSerializer(serializers.Serializer):

    month = serializers.DateField()

    sales_taxable = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    sales_gst = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    purchase_taxable = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    purchase_gst = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    gst_payable = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )


class HSNSerializer(serializers.Serializer):

    hsn_code = serializers.CharField()

    product = serializers.CharField()

    quantity = serializers.IntegerField()

    taxable_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    gst_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )


class GSTRateSerializer(serializers.Serializer):

    gst_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    taxable_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    gst_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )