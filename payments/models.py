from django.db import models

from masters.models import Customer, Supplier
from django.utils import timezone

class CustomerPayment(models.Model):

    PAYMENT_MODE = (
        ("Cash", "Cash"),
        ("Bank", "Bank"),
    )

    receipt_number = models.PositiveIntegerField(
        unique=True,
        editable=False,
        blank=True,
        null=True,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    payment_date = models.DateField(
     default=timezone.localdate,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    payment_mode = models.CharField(
        max_length=10,
        choices=PAYMENT_MODE,
        default="Cash",
    )

    remarks = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-receipt_number"]

    @property
    def display_receipt_number(self):
        if self.receipt_number:
            return f"{self.receipt_number:02d}"
        return "--"

    def __str__(self):
        return self.display_receipt_number
    
class SupplierPayment(models.Model):

    PAYMENT_MODE = (
        ("Cash", "Cash"),
        ("Bank", "Bank"),
    )

    receipt_number = models.PositiveIntegerField(
        unique=True,
        editable=False,
        blank=True,
        null=True,
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    payment_date = models.DateField(
     default=timezone.localdate,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    payment_mode = models.CharField(
        max_length=10,
        choices=PAYMENT_MODE,
        default="Cash",
    )

    remarks = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-receipt_number"]

    @property
    def display_receipt_number(self):
        if self.receipt_number:
            return f"{self.receipt_number:02d}"
        return "--"

    def __str__(self):
        return self.display_receipt_number