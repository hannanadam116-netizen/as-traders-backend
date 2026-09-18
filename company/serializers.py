from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company

        fields = (
            "id",

            "company_name",
            "proprietor_name",

            "gst_number",
            "pan_number",

            "address",
            "city",
            "state",
            "pin_code",

            "mobile",
            "email",
            "website",

            "bank_name",
            "account_number",
            "ifsc_code",
            "upi_id",

            "invoice_prefix",
            "purchase_prefix",
            "financial_year",

            "terms",

            "logo",

            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "created_at",
            "updated_at",
        )