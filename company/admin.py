from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "proprietor_name",
        "mobile",
        "gst_number",
        "financial_year",
    )

    search_fields = (
        "company_name",
        "proprietor_name",
        "gst_number",
    )

    fieldsets = (

        ("Company Details", {
            "fields": (
                "company_name",
                "proprietor_name",
                "logo",
            )
        }),

        ("Address", {
            "fields": (
                "address",
                "city",
                "state",
                "pin_code",
            )
        }),

        ("Contact", {
            "fields": (
                "mobile",
                "email",
                "website",
            )
        }),

        ("GST & PAN", {
            "fields": (
                "gst_number",
                "pan_number",
            )
        }),

        ("Bank Details", {
            "fields": (
                "bank_name",
                "account_number",
                "ifsc_code",
                "upi_id",
            )
        }),

        ("Invoice Settings", {
            "fields": (
                "invoice_prefix",
                "purchase_prefix",
                "financial_year",
            )
        }),

        ("Terms & Conditions", {
            "fields": (
                "terms",
            )
        }),

    )

    def has_add_permission(self, request):
        """
        Allow only one company record.
        """
        return Company.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting the company.
        """
        return False