from django.db import models
from masters.models import Supplier, Product


class PurchaseInvoice(models.Model):

    PAYMENT_CHOICES = (
        ("Cash", "Cash"),
        ("Credit", "Credit"),
    )

    invoice_number = models.PositiveIntegerField(
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchase_invoices",
    )

    invoice_date = models.DateField()

    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default="Cash",
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    transport_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    gst_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    gst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    grand_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-invoice_number"]

    @property
    def display_invoice_number(self):
        if self.invoice_number:
            return f"{self.invoice_number:02d}"
        return "--"

    def __str__(self):
        return self.display_invoice_number


class PurchaseInvoiceItem(models.Model):

    invoice = models.ForeignKey(
        PurchaseInvoice,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    gst_percent = models.DecimalField(
      max_digits=5,
      decimal_places=2,
      default=0,
    )

    gst_amount = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ["product__product_name"]

    def __str__(self):
        return (
            f"{self.invoice.display_invoice_number}"
            f" - {self.product.product_name}"
        )