from decimal import Decimal

from django.db import transaction
from django.db.models import F, Max

from masters.models import (
    CustomerProductPrice,
)

from .models import (
    SalesInvoice,
    SalesInvoiceItem,
)


class SalesService:

    @staticmethod
    def _get_next_invoice_number():

        last = SalesInvoice.objects.aggregate(
            Max("invoice_number")
        )["invoice_number__max"]

        if last is None:
            return 1

        return last + 1

    @staticmethod
    def _get_customer_price(customer, product):

        try:
            return CustomerProductPrice.objects.get(
                customer=customer,
                product=product
            ).selling_price

        except CustomerProductPrice.DoesNotExist:
            return product.default_selling_price

    @staticmethod
    def _calculate_item(
     customer,
     product,
     quantity,
     selling_price=None,
    ):

        quantity = int(quantity)

        purchase_price = product.purchase_price

        if selling_price is None:

         selling_price = SalesService._get_customer_price(
          customer,
          product,
         )

        gst_percent = Decimal("0.00")

        total = Decimal(quantity) * selling_price

        profit = (
            selling_price - purchase_price
        ) * Decimal(quantity)

        return {
            "purchase_price": purchase_price,
            "selling_price": selling_price,
            "gst_percent": gst_percent,
            "total": total,
            "profit": profit,
        }

    @staticmethod
    def _calculate_totals(
        subtotal,
        discount,
        transport_charge,
        gst_percent,
        total_profit,
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

        return (
            subtotal,
            gst_amount,
            grand_total,
            total_profit,
        )

    @staticmethod
    def _update_stock(product, quantity):

        product.current_stock -= quantity
        product.save(
            update_fields=["current_stock"]
        )

    @staticmethod
    def _update_customer_balance(
        customer,
        amount,
        payment_type,
    ):

        if payment_type != "Credit":
            return

        customer.current_balance = (
            customer.current_balance + amount
        )

        customer.save(
            update_fields=["current_balance"]
        )
    
    @staticmethod
    def _restore_stock(invoice):

     for item in invoice.items.select_related("product"):

        product = item.product

        product.current_stock += item.quantity

        product.save(
            update_fields=["current_stock"]
        )

    @staticmethod
    def _restore_customer_balance(invoice):

     if invoice.payment_type != "Credit":
        return

     customer = invoice.customer

     customer.current_balance -= invoice.grand_total

     customer.save(
        update_fields=["current_balance"]
    )
    @staticmethod
    @transaction.atomic
    def create_invoice(data):

        customer = data["customer"]

        invoice = SalesInvoice.objects.create(
            invoice_number=SalesService._get_next_invoice_number(),
            customer=customer,
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
        total_profit = Decimal("0.00")
        for row in data["items"]:

            product = row["product"]
            quantity = row["quantity"]
            selling_price = row.get("selling_price")

            values = SalesService._calculate_item(
                customer=customer,
                product=product,
                quantity=quantity,
                selling_price=selling_price,
            )

            SalesInvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=quantity,
                purchase_price=values["purchase_price"],
                selling_price=values["selling_price"],
                gst_percent=values["gst_percent"],
                total=values["total"],
                profit=values["profit"],
            )

            subtotal += values["total"]
            total_profit += values["profit"]

            SalesService._update_stock(
                product,
                quantity,
            )
            if selling_price is not None:
             product.default_selling_price = selling_price
             product.save(
              update_fields=["default_selling_price"]
             )

        (
            invoice.subtotal,
            invoice.gst_amount,
            invoice.grand_total,
            invoice.total_profit,
        ) = SalesService._calculate_totals(
            subtotal=subtotal,
            discount=invoice.discount,
            transport_charge=invoice.transport_charge,
            gst_percent=invoice.gst_percent,
            total_profit=total_profit,
        )

        invoice.save(
            update_fields=[
                "subtotal",
                "gst_amount",
                "grand_total",
                "total_profit",
            ]
        )

        SalesService._update_customer_balance(
            customer=customer,
            amount=invoice.grand_total,
            payment_type=invoice.payment_type,
        )

        return invoice
    
    @staticmethod
    @transaction.atomic
    def update_invoice(
        invoice,
        data,
    ):

        SalesService._restore_stock(
            invoice
        )

        SalesService._restore_customer_balance(
            invoice
        )

        invoice.items.all().delete()

        customer = data["customer"]

        invoice.customer = customer
        invoice.invoice_date = data.get(
           "invoice_date",
           invoice.invoice_date,
        )

        invoice.payment_type = data[
            "payment_type"
        ]

        invoice.discount = data.get(
            "discount",
            Decimal("0.00")
        )

        invoice.transport_charge = data.get(
            "transport_charge",
            Decimal("0.00")
        )

        invoice.gst_percent = data.get(
            "gst_percent",
            Decimal("0.00")
        )

        subtotal = Decimal("0.00")

        total_profit = Decimal("0.00")

        for row in data["items"]:

            product = row["product"]

            quantity = row["quantity"]
            selling_price = row.get("selling_price")
            values = SalesService._calculate_item(
                customer=customer,
                product=product,
                quantity=quantity,
                selling_price=selling_price,
            )

            SalesInvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=quantity,
                purchase_price=values[
                    "purchase_price"
                ],
                selling_price=values[
                    "selling_price"
                ],
                gst_percent=values[
                    "gst_percent"
                ],
                total=values["total"],
                profit=values["profit"],
            )

            subtotal += values["total"]

            total_profit += values[
                "profit"
            ]

            SalesService._update_stock(
                product,
                quantity,
            )
            if selling_price is not None:
             product.default_selling_price = selling_price
             product.save(
              update_fields=["default_selling_price"]
             )

        (
            invoice.subtotal,
            invoice.gst_amount,
            invoice.grand_total,
            invoice.total_profit,
        ) = SalesService._calculate_totals(
            subtotal=subtotal,
            discount=invoice.discount,
            transport_charge=invoice.transport_charge,
            gst_percent=invoice.gst_percent,
            total_profit=total_profit,
        )

        invoice.save(
            update_fields=[
                "customer",
                "payment_type",
                "discount",
                "transport_charge",
                "gst_percent",
                "subtotal",
                "gst_amount",
                "grand_total",
                "total_profit",
            ]
        )

        SalesService._update_customer_balance(
            customer=customer,
            amount=invoice.grand_total,
            payment_type=invoice.payment_type,
        )

        return invoice
    @staticmethod
    @transaction.atomic
    def delete_invoice(
        invoice,
    ):

        SalesService._restore_stock(
            invoice
        )

        SalesService._restore_customer_balance(
            invoice
        )

        invoice.delete()