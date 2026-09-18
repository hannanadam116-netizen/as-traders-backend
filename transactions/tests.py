from decimal import Decimal

from django.test import TestCase

from masters.models import (
    Category,
    Customer,
    Product,
)

from transactions.services import SalesService


class SalesServiceTest(TestCase):

    def setUp(self):

        category = Category.objects.create(
            name="Sugar"
        )

        self.customer = Customer.objects.create(
            name="Test Customer"
        )

        self.product = Product.objects.create(
            product_name="Sugar",
            category=category,
            purchase_price=Decimal("2230"),
            default_selling_price=Decimal("2270"),
            current_stock=100,
        )

    def test_create_invoice(self):

        invoice = SalesService.create_invoice({

            "customer": self.customer,

            "payment_type": "Cash",

            "discount": Decimal("100"),

            "transport_charge": Decimal("50"),

            "gst_percent": Decimal("5"),

            "items": [
                {
                    "product": self.product,
                    "quantity": 10,
                }
            ]
        })

        self.assertEqual(invoice.invoice_number, 1)

        self.assertEqual(
            invoice.subtotal,
            Decimal("22700")
        )

        self.assertEqual(
            invoice.total_profit,
            Decimal("400")
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.current_stock,
            90
        )
