from django.db import models

from masters.models import Product


class StockTransaction(models.Model):

    TRANSACTION_TYPES = (
        ("OPENING", "Opening Stock"),
        ("PURCHASE", "Purchase"),
        ("SALE", "Sale"),
        ("ADJUSTMENT_IN", "Adjustment In"),
        ("ADJUSTMENT_OUT", "Adjustment Out"),
        ("DAMAGED", "Damaged"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_transactions",
    )

    transaction_date = models.DateField(
        auto_now_add=True,
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
    )

    quantity = models.IntegerField()

    balance_stock = models.IntegerField()

    reference_number = models.CharField(
        max_length=100,
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "-transaction_date",
            "-id",
        ]

    def __str__(self):
        return (
            f"{self.product.product_name} - "
            f"{self.transaction_type} "
            f"({self.quantity})"
        )