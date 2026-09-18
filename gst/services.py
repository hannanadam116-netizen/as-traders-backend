from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncMonth

from transactions.models import (
    SalesInvoice,
    SalesInvoiceItem,
)

from purchases.models import (
    PurchaseInvoice,
    PurchaseInvoiceItem,
)


class GSTService:

    # =====================================================
    # GST SUMMARY
    # =====================================================

    @staticmethod
    def gst_summary():

        sales = SalesInvoice.objects.aggregate(
            taxable=Sum("subtotal"),
            gst=Sum("gst_amount"),
        )

        purchases = PurchaseInvoice.objects.aggregate(
            taxable=Sum("subtotal"),
            gst=Sum("gst_amount"),
        )

        sales_taxable = sales["taxable"] or Decimal("0.00")
        sales_gst = sales["gst"] or Decimal("0.00")

        purchase_taxable = purchases["taxable"] or Decimal("0.00")
        purchase_gst = purchases["gst"] or Decimal("0.00")

        return {

            "sales_taxable": sales_taxable,

            "sales_gst": sales_gst,

            "purchase_taxable": purchase_taxable,

            "purchase_gst": purchase_gst,

            "gst_payable": sales_gst - purchase_gst,

        }

    # =====================================================
    # MONTHLY GST SUMMARY
    # =====================================================

    @staticmethod
    def monthly_gst_summary():

        sales = (
            SalesInvoice.objects
            .annotate(month=TruncMonth("invoice_date"))
            .values("month")
            .annotate(
                sales_taxable=Sum("subtotal"),
                sales_gst=Sum("gst_amount"),
            )
            .order_by("month")
        )

        purchases = (
            PurchaseInvoice.objects
            .annotate(month=TruncMonth("invoice_date"))
            .values("month")
            .annotate(
                purchase_taxable=Sum("subtotal"),
                purchase_gst=Sum("gst_amount"),
            )
            .order_by("month")
        )

        purchase_map = {
            row["month"]: row
            for row in purchases
        }

        result = []

        for sale in sales:

            purchase = purchase_map.get(
                sale["month"],
                {},
            )

            sales_taxable = sale["sales_taxable"] or Decimal("0.00")
            sales_gst = sale["sales_gst"] or Decimal("0.00")

            purchase_taxable = (
                purchase.get("purchase_taxable")
                or Decimal("0.00")
            )

            purchase_gst = (
                purchase.get("purchase_gst")
                or Decimal("0.00")
            )

            result.append({

                "month": sale["month"],

                "sales_taxable": sales_taxable,

                "sales_gst": sales_gst,

                "purchase_taxable": purchase_taxable,

                "purchase_gst": purchase_gst,

                "gst_payable": sales_gst - purchase_gst,

            })

        return result
    
        # =====================================================
    # HSN SUMMARY
    # =====================================================

    @staticmethod
    def hsn_summary():

        items = (
            SalesInvoiceItem.objects
            .select_related("product")
            .values(
                "product__hsn_code",
                "product__product_name",
            )
            .annotate(
                quantity=Sum("quantity"),
                taxable_value=Sum("total"),
            )
            .order_by(
                "product__hsn_code",
                "product__product_name",
            )
        )

        result = []

        for item in items:

            taxable = item["taxable_value"] or Decimal("0.00")

            result.append({

                "hsn_code":
                    item["product__hsn_code"] or "",

                "product":
                    item["product__product_name"],

                "quantity":
                    item["quantity"] or 0,

                "taxable_value":
                    taxable,

                "gst_amount":
                    Decimal("0.00"),

            })

        return result


    # =====================================================
    # GST RATE SUMMARY
    # =====================================================

    @staticmethod
    def gst_rate_summary():

        items = (
            SalesInvoiceItem.objects
            .values("gst_percent")
            .annotate(
                quantity=Sum("quantity"),
                taxable_value=Sum("total"),
            )
            .order_by("gst_percent")
        )

        result = []

        for item in items:

            taxable = item["taxable_value"] or Decimal("0.00")

            gst_rate = item["gst_percent"] or Decimal("0.00")

            gst_amount = (
                taxable * gst_rate
            ) / Decimal("100")

            result.append({

                "gst_rate": gst_rate,

                "quantity":
                    item["quantity"] or 0,

                "taxable_value": taxable,

                "gst_amount": gst_amount,

            })

        return result
    
        # =====================================================
    # GSTR-1 SUMMARY
    # =====================================================

    @staticmethod
    def gstr1_summary():

        invoices = (
            SalesInvoice.objects
            .select_related("customer")
            .prefetch_related("items")
            .order_by("-invoice_date")
        )

        result = []

        for invoice in invoices:

            result.append({

                "invoice_number":
                    invoice.display_invoice_number,

                "invoice_date":
                    invoice.invoice_date,

                "customer":
                    invoice.customer.name,

                "gst_number":
                    invoice.customer.gst_number,

                "taxable_value":
                    invoice.subtotal,

                "gst_amount":
                    invoice.gst_amount,

                "invoice_total":
                    invoice.grand_total,

            })

        return result


    # =====================================================
    # GSTR-3B SUMMARY
    # =====================================================

    @staticmethod
    def gstr3b_summary():

        summary = GSTService.gst_summary()

        return {

            "outward_taxable_supply":
                summary["sales_taxable"],

            "outward_tax":
                summary["sales_gst"],

            "inward_taxable_supply":
                summary["purchase_taxable"],

            "input_tax_credit":
                summary["purchase_gst"],

            "net_gst_payable":
                summary["gst_payable"],

        }
    
        # =====================================================
    # INPUT TAX CREDIT SUMMARY
    # =====================================================

    @staticmethod
    def input_tax_credit_summary():

        purchases = (
            PurchaseInvoice.objects
            .values("payment_type")
            .annotate(

                taxable_value=Sum("subtotal"),

                gst_amount=Sum("gst_amount"),

                invoice_count=Sum("id"),

            )
            .order_by("payment_type")
        )

        result = []

        total_itc = Decimal("0.00")

        for purchase in purchases:

            gst_amount = purchase["gst_amount"] or Decimal("0.00")

            total_itc += gst_amount

            result.append({

                "payment_type":
                    purchase["payment_type"],

                "taxable_value":
                    purchase["taxable_value"] or Decimal("0.00"),

                "gst_amount":
                    gst_amount,

            })

        return {

            "total_input_tax_credit": total_itc,

            "details": result,

        }


    # =====================================================
    # OUTPUT TAX SUMMARY
    # =====================================================

    @staticmethod
    def output_tax_summary():

        sales = (
            SalesInvoice.objects
            .values("payment_type")
            .annotate(

                taxable_value=Sum("subtotal"),

                gst_amount=Sum("gst_amount"),

                invoice_count=Sum("id"),

            )
            .order_by("payment_type")
        )

        result = []

        total_output_tax = Decimal("0.00")

        for sale in sales:

            gst_amount = sale["gst_amount"] or Decimal("0.00")

            total_output_tax += gst_amount

            result.append({

                "payment_type":
                    sale["payment_type"],

                "taxable_value":
                    sale["taxable_value"] or Decimal("0.00"),

                "gst_amount":
                    gst_amount,

            })

        return {

            "total_output_tax": total_output_tax,

            "details": result,

        }


    # =====================================================
    # GST DASHBOARD
    # =====================================================

    @staticmethod
    def gst_dashboard():

        gst = GSTService.gst_summary()

        input_tax = GSTService.input_tax_credit_summary()

        output_tax = GSTService.output_tax_summary()

        return {

            "sales_taxable":
                gst["sales_taxable"],

            "purchase_taxable":
                gst["purchase_taxable"],

            "sales_gst":
                gst["sales_gst"],

            "purchase_gst":
                gst["purchase_gst"],

            "gst_payable":
                gst["gst_payable"],

            "input_tax_credit":
                input_tax["total_input_tax_credit"],

            "output_tax":
                output_tax["total_output_tax"],

        }
    
        # =====================================================
    # GST RECONCILIATION
    # =====================================================

    @staticmethod
    def gst_reconciliation():

        summary = GSTService.gst_summary()

        return {

            "output_tax": summary["sales_gst"],

            "input_tax_credit": summary["purchase_gst"],

            "net_gst_payable": summary["gst_payable"],

            "status": (
                "Payable"
                if summary["gst_payable"] >= 0
                else "Refund"
            ),
        }


    # =====================================================
    # MONTHLY GST CHART
    # =====================================================

    @staticmethod
    def monthly_gst_chart():

        monthly = GSTService.monthly_gst_summary()

        labels = []
        output_gst = []
        input_gst = []

        for row in monthly:

            month = row["month"]

            if month:
                labels.append(month.strftime("%b %Y"))
            else:
                labels.append("Unknown")

            output_gst.append(row["sales_gst"])
            input_gst.append(row["purchase_gst"])

        return {

            "labels": labels,

            "output_gst": output_gst,

            "input_gst": input_gst,

        }