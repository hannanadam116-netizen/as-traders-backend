from django.db import models


class BusinessProfile(models.Model):
    business_name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=100)

    gst_number = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=20, blank=True)

    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    address = models.TextField()

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    logo = models.ImageField(upload_to='business_logo/', blank=True, null=True)

    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=30, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    upi_id = models.CharField(max_length=100, blank=True)

    invoice_prefix = models.CharField(max_length=10, default="INV")

    currency = models.CharField(max_length=10, default="INR")

    financial_year = models.CharField(max_length=20, default="2026-27")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business Profile"
        verbose_name_plural = "Business Profile"

    def __str__(self):
        return self.business_name