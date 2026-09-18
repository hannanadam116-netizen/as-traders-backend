from django.db import models


class Company(models.Model):

    company_name = models.CharField(
        max_length=200
    )

    proprietor_name = models.CharField(
        max_length=200
    )

    gst_number = models.CharField(
        max_length=20,
        blank=True
    )

    pan_number = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pin_code = models.CharField(
        max_length=10
    )

    mobile = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    website = models.CharField(
        max_length=200,
        blank=True
    )

    bank_name = models.CharField(
        max_length=200,
        blank=True
    )

    account_number = models.CharField(
        max_length=50,
        blank=True
    )

    ifsc_code = models.CharField(
        max_length=20,
        blank=True
    )

    upi_id = models.CharField(
        max_length=100,
        blank=True
    )

    invoice_prefix = models.CharField(
        max_length=10,
        default="INV"
    )

    purchase_prefix = models.CharField(
        max_length=10,
        default="PUR"
    )

    financial_year = models.CharField(
        max_length=20,
        default="2026-27"
    )

    terms = models.TextField(
        blank=True
    )

    logo = models.ImageField(
        upload_to="company/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company"

    def __str__(self):
        return self.company_name