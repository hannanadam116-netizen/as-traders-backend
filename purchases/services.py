from decimal import Decimal

from django.db import transaction
from django.db.models import Max

from masters.models import Supplier, Product
from django.db.models import F
from .models import (
    PurchaseInvoice,
    PurchaseInvoiceItem,
)


class PurchaseService:

    @staticmethod
    def _get_next_invoice_number():

        last_invoice = PurchaseInvoice.objects.aggregate(
            Max("invoice_number")
        )["invoice_number__max"]

        if last_invoice is None:
            return 1

        return last_invoice + 1

    @staticmethod
    def _calculate_item(
        product,
        quantity,
        purchase_price,
    ):

        quantity = int(quantity)

        purchase_price = Decimal(purchase_price)

        total = purchase_price * Decimal(quantity)

        return {
            "purchase_price": purchase_price,
            "total": total,
        }

    @staticmethod
    def _calculate_totals(
        subtotal,
        discount,
        transport_charge,
        gst_percent,
    ):

        taxable_amount = (
            subtotal
            - discount
            + transport_charge
        )

        gst_amount = (
            taxable_amount
            * gst_percent
            / Decimal("100")
        )

        grand_total = taxable_amount + gst_amount

        return {
            "subtotal": subtotal,
            "gst_amount": gst_amount,
            "grand_total": grand_total,
        }

    @staticmethod
    def _update_stock(
     product,
     quantity,
     purchase_price,
    ):
     """
    Increase stock and update latest purchase price.
    """

     Product.objects.filter(
        pk=product.pk
     ).update(
        current_stock=F("current_stock") + quantity,
        purchase_price=purchase_price,
     )

    @staticmethod
    def _update_supplier_balance(
     supplier,
     amount,
     payment_type,
):
     if payment_type != "Credit":
        return

     Supplier.objects.filter(
        pk=supplier.pk
     ).update(
        current_balance=F("current_balance") + amount
     )
    @staticmethod
    def _restore_stock(invoice):

     for item in invoice.items.select_related("product"):

        Product.objects.filter(
            pk=item.product.pk
        ).update(
            current_stock=F("current_stock") - item.quantity,
        )

    @staticmethod
    def _restore_supplier_balance(invoice):

     if invoice.payment_type != "Credit":
        return

     Supplier.objects.filter(
        pk=invoice.supplier_id
     ).update(
        current_balance=F("current_balance") - invoice.grand_total
    )

    @staticmethod
    @transaction.atomic
    def create_purchase_invoice(data):

        supplier = data["supplier"]

        invoice = PurchaseInvoice.objects.create(
            invoice_number=PurchaseService._get_next_invoice_number(),
            supplier=supplier,
            invoice_date=data.get("invoice_date"),
            payment_type=data["payment_type"],
            discount=data.get(
                "discount",
                Decimal("0.00")
            ),
            transport_charge=data.get(
                "transport_charge",
                Decimal("0.00")
            ),
            gst_percent=data.get(
                "gst_percent",
                Decimal("0.00")
            ),
        )

        subtotal = Decimal("0.00")
        for row in data["items"]:

            product = row["product"]
            quantity = int(row["quantity"])
            purchase_price = Decimal(row["purchase_price"])

            values = PurchaseService._calculate_item(
                product=product,
                quantity=quantity,
                purchase_price=purchase_price,
            )

            PurchaseInvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=quantity,
                purchase_price=values["purchase_price"],
                total=values["total"],
            )

            subtotal += values["total"]

            PurchaseService._update_stock(
                product=product,
                quantity=quantity,
                purchase_price=purchase_price,
            )

        totals = PurchaseService._calculate_totals(
            subtotal=subtotal,
            discount=invoice.discount,
            transport_charge=invoice.transport_charge,
            gst_percent=invoice.gst_percent,
        )

        invoice.subtotal = totals["subtotal"]
        invoice.gst_amount = totals["gst_amount"]
        invoice.grand_total = totals["grand_total"]

        invoice.save(
            update_fields=[
                "subtotal",
                "gst_amount",
                "grand_total",
            ]
        )

        PurchaseService._update_supplier_balance(
            supplier=supplier,
            amount=invoice.grand_total,
            payment_type=invoice.payment_type,
        )

        return invoice
    
    @staticmethod
    @transaction.atomic
    def update_purchase_invoice(
        invoice,
        data,
    ):

        # -----------------------------------------
        # Restore previous effects
        # -----------------------------------------

        PurchaseService._restore_stock(
            invoice,
        )

        PurchaseService._restore_supplier_balance(
            invoice,
        )

        invoice.items.all().delete()

        # -----------------------------------------
        # Update invoice
        # -----------------------------------------

        supplier = data["supplier"]

        invoice.supplier = supplier
        invoice.invoice_date = data.get(
         "invoice_date",
         invoice.invoice_date,
        )

        invoice.payment_type = data["payment_type"]

        invoice.discount = data.get(
            "discount",
            Decimal("0.00"),
        )

        invoice.transport_charge = data.get(
            "transport_charge",
            Decimal("0.00"),
        )

        invoice.gst_percent = data.get(
            "gst_percent",
            Decimal("0.00"),
        )

        subtotal = Decimal("0.00")

        # -----------------------------------------
        # Recreate Items
        # -----------------------------------------

        for row in data["items"]:

            product = row["product"]

            quantity = int(
                row["quantity"]
            )

            purchase_price = Decimal(
                row["purchase_price"]
            )

            values = PurchaseService._calculate_item(
                product=product,
                quantity=quantity,
                purchase_price=purchase_price,
            )

            PurchaseInvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=quantity,
                purchase_price=values["purchase_price"],
                total=values["total"],
            )

            subtotal += values["total"]

            PurchaseService._update_stock(
                product=product,
                quantity=quantity,
                purchase_price=purchase_price,
            )

        totals = PurchaseService._calculate_totals(
            subtotal=subtotal,
            discount=invoice.discount,
            transport_charge=invoice.transport_charge,
            gst_percent=invoice.gst_percent,
        )

        invoice.subtotal = totals["subtotal"]

        invoice.gst_amount = totals["gst_amount"]

        invoice.grand_total = totals["grand_total"]

        invoice.save(
    update_fields=[
        "supplier",
        "invoice_date",
        "payment_type",
        "discount",
        "transport_charge",
        "gst_percent",
        "subtotal",
        "gst_amount",
        "grand_total",
    ]
)

        PurchaseService._update_supplier_balance(
            supplier=supplier,
            amount=invoice.grand_total,
            payment_type=invoice.payment_type,
        )

        return invoice    
    @staticmethod
    @transaction.atomic
    def delete_purchase_invoice(
        invoice,
    ):

        # -----------------------------------------
        # Restore stock
        # -----------------------------------------

        PurchaseService._restore_stock(
            invoice,
        )

        # -----------------------------------------
        # Restore supplier balance
        # -----------------------------------------

        PurchaseService._restore_supplier_balance(
            invoice,
        )

        # -----------------------------------------
        # Delete invoice
        # -----------------------------------------

        invoice.delete()