from decimal import Decimal
from datetime import timedelta
from django.db.models import (
    Sum,
    Count,
    F,
    DecimalField,
    ExpressionWrapper,
)
from django.db.models.functions import (
    Coalesce,
    TruncMonth,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta
from masters.models import (
    Product,
    Customer,
    Supplier,
)

from transactions.models import (
    SalesInvoice,
    SalesInvoiceItem,
)

from purchases.models import (
    PurchaseInvoice,
    PurchaseInvoiceItem,
)

from payments.models import (
    CustomerPayment,
    SupplierPayment,
)

from .excel import (
    export_sales_excel,
    export_purchase_excel,
    export_stock_excel,
    export_customer_ledger_excel,
    export_supplier_ledger_excel,
    export_profit_excel,
    export_customer_sales_excel,
    export_product_sales_excel,
)
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDate,Coalesce
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response


# ==========================================================
# SALES REPORT
# ==========================================================

class SalesReportView(APIView):

    def get(self, request):

        invoices = (
            SalesInvoice.objects
            .select_related("customer")
            .order_by("-invoice_date", "-invoice_number")
        )
        today = timezone.localdate()

        period = request.GET.get("period")

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        customer = request.GET.get("customer")

# -----------------------------------------
# Date Filter
# -----------------------------------------

        month_map = {
         "jan": 1,
         "feb": 2,
         "mar": 3,
         "apr": 4,
         "may": 5,
         "jun": 6,
         "jul": 7,
         "aug": 8,
         "sep": 9,
         "oct": 10,
         "nov": 11,
         "dec": 12,
        }

        if from_date and to_date:

         invoices = invoices.filter(
          invoice_date__range=[from_date, to_date]
         )

        elif period in month_map:

         invoices = invoices.filter(
          invoice_date__year=today.year,
           invoice_date__month=month_map[period],
          )

        elif period == "year":

         invoices = invoices.filter(
          invoice_date__year=today.year
         )

        elif period == "last_month":

         first_day = today.replace(day=1)

         last_month = first_day - timedelta(days=1)

         invoices = invoices.filter(
          invoice_date__year=last_month.year,
          invoice_date__month=last_month.month,
         )

        else:
    # Default = This Month
         invoices = invoices.filter(
           invoice_date__year=today.year,
           invoice_date__month=today.month,
         )

# -----------------------------------------
# Customer Filter
# -----------------------------------------

        if customer:

          invoices = invoices.filter(
           customer_id=customer
        )

        summary = invoices.aggregate(

            total_sales=Coalesce(
                Sum("grand_total"),
                Decimal("0.00")
            ),

            total_profit=Coalesce(
                Sum("total_profit"),
                Decimal("0.00")
            ),

            total_invoices=Count("id")

        )

        results = []

        for invoice in invoices:

            results.append({

                "id": invoice.id,

                "invoice_number":
                invoice.display_invoice_number,

                "date":
                invoice.invoice_date,

                "customer":
                invoice.customer.name,

                "payment_type":
                invoice.payment_type,

                "subtotal":
                invoice.subtotal,

                "discount":
                invoice.discount,

                "gst":
                invoice.gst_amount,

                "grand_total":
                invoice.grand_total,

                "profit":
                invoice.total_profit,

            })

        return Response({

            "summary": summary,

            "results": results,

        })


# ==========================================================
# PURCHASE REPORT
# ==========================================================


class PurchaseReportView(APIView):

    def get(self, request):

        invoices = (
            PurchaseInvoice.objects
            .select_related("supplier")
            .order_by("-invoice_date", "-invoice_number")
        )

        today = timezone.localdate()

        period = request.GET.get("period", "month")

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        supplier = request.GET.get("supplier")

        # -----------------------------------------
        # Period / Date Filter
        # -----------------------------------------

        if from_date and to_date:

            invoices = invoices.filter(
                invoice_date__range=[from_date, to_date]
            )

        elif period == "year":

            invoices = invoices.filter(
                invoice_date__year=today.year,
            )

        elif period == "last_month":

            first_day = today.replace(day=1)

            last_month = first_day - timedelta(days=1)

            invoices = invoices.filter(
                invoice_date__year=last_month.year,
                invoice_date__month=last_month.month,
            )

        else:

            invoices = invoices.filter(
                invoice_date__year=today.year,
                invoice_date__month=today.month,
            )

        # -----------------------------------------
        # Supplier Filter
        # -----------------------------------------

        if supplier:

            invoices = invoices.filter(
                supplier_id=supplier
            )

        # -----------------------------------------
        # Summary
        # -----------------------------------------

        summary = invoices.aggregate(

            total_purchase=Coalesce(
                Sum("grand_total"),
                Decimal("0.00"),
            ),

            total_invoices=Count("id"),

        )

        # -----------------------------------------
        # Results
        # -----------------------------------------

        results = []

        for invoice in invoices:

            results.append({

                "id": invoice.id,

                "invoice_number":
                    invoice.display_invoice_number,

                "date":
                    invoice.invoice_date,

                "supplier":
                    invoice.supplier.name,

                "payment_type":
                    invoice.payment_type,

                "subtotal":
                    invoice.subtotal,

                "discount":
                    invoice.discount,

                "gst":
                    invoice.gst_amount,

                "grand_total":
                    invoice.grand_total,

            })

        return Response({

            "summary": summary,

            "results": results,

        })


# ==========================================================
# CUSTOMER WISE SALES REPORT
# ==========================================================

class CustomerWiseSalesView(APIView):

    def get(self, request):

        customers = (

            SalesInvoice.objects

            .values(

                "customer",

                "customer__name",

            )

            .annotate(

                total_sales=Coalesce(
                    Sum("grand_total"),
                    Decimal("0.00")
                ),

                total_profit=Coalesce(
                    Sum("total_profit"),
                    Decimal("0.00")
                ),

                invoices=Count("id"),

            )

            .order_by("-total_sales")

        )

        summary = {

            "customers": customers.count(),

            "sales":

            customers.aggregate(

                total=Coalesce(
                    Sum("total_sales"),
                    Decimal("0.00")
                )

            )["total"]

        }

        return Response({

            "summary": summary,

            "results": customers,

        })


# ==========================================================
# CUSTOMER WISE PROFIT REPORT
# ==========================================================

class CustomerWiseProfitView(APIView):

    def get(self, request):

        customers = (

            SalesInvoice.objects

            .values(

                "customer",

                "customer__name",

            )

            .annotate(

                total_profit=Coalesce(

                    Sum("total_profit"),

                    Decimal("0.00")

                )

            )

            .order_by("-total_profit")

        )

        results = []

        for row in customers:

         results.append({

         "customer": row["customer__name"],

         "profit": row["total_profit"],

        })

        return Response({

         "summary": {

         "customers": len(results),

        },

        "results": results,

    })
    
# ==========================================================
# PRODUCT WISE SALES REPORT
# ==========================================================

class ProductWiseSalesView(APIView):

    def get(self, request):

        products = (

            SalesInvoiceItem.objects

            .values(

                "product",

                "product__product_name",

            )

            .annotate(

                quantity=Coalesce(
                    Sum("quantity"),
                    0,
                ),

                sales=Coalesce(
                    Sum("total"),
                    Decimal("0.00"),
                ),

                profit=Coalesce(
                    Sum("profit"),
                    Decimal("0.00"),
                ),

            )

            .order_by("-sales")

        )

        summary = {

            "products": products.count(),

            "total_sales":

            products.aggregate(

                total=Coalesce(

                    Sum("sales"),

                    Decimal("0.00")

                )

            )["total"],

            "total_profit":

            products.aggregate(

                total=Coalesce(

                    Sum("profit"),

                    Decimal("0.00")

                )

            )["total"]

        }

        return Response({

            "summary": summary,

            "results": products,

        })


# ==========================================================
# PRODUCT WISE PROFIT REPORT
# ==========================================================

class ProductWiseProfitView(APIView):

    def get(self, request):

        products = (

            SalesInvoiceItem.objects

            .values(

                "product",

                "product__product_name",

            )

            .annotate(

                quantity=Coalesce(

                    Sum("quantity"),

                    0,

                ),

                profit=Coalesce(

                    Sum("profit"),

                    Decimal("0.00"),

                ),

            )

            .order_by("-profit")

        )

        results = []

        for row in products:

         results.append({

          "product": row["product__product_name"],

          "quantity": row["quantity"],

          "profit": row["profit"],

        })

        return Response({

         "summary": {

          "products": len(results),

         },

         "results": results,

        })


# ==========================================================
# CUSTOMER LEDGER
# ==========================================================

class CustomerLedgerView(APIView):

    def get(self, request):

        customer_id = request.GET.get("customer")

        customers = Customer.objects.filter(
            is_active=True
        )

        if customer_id:
            customers = customers.filter(
                id=customer_id
            )

        results = []

        total_sales = Decimal("0.00")
        total_received = Decimal("0.00")
        total_balance = Decimal("0.00")

        for customer in customers:

            sales = SalesInvoice.objects.filter(
                customer=customer
            ).aggregate(
                total=Coalesce(
                    Sum("grand_total"),
                    Decimal("0.00")
                )
            )["total"]

            received = CustomerPayment.objects.filter(
                customer=customer
            ).aggregate(
                total=Coalesce(
                    Sum("amount"),
                    Decimal("0.00")
                )
            )["total"]

            balance = customer.current_balance

            total_sales += sales
            total_received += received
            total_balance += balance

            results.append({

                "customer": customer.name,

                "sales": sales,

                "received": received,

                "balance": balance,

            })

        return Response({

            "summary": {

                "customers": len(results),

                "sales": total_sales,

                "received": total_received,

                "balance": total_balance,

            },

            "results": results,

        })


# ==========================================================
# SUPPLIER LEDGER
# ==========================================================

class SupplierLedgerView(APIView):

    def get(self, request):

        supplier_id = request.GET.get("supplier")

        suppliers = Supplier.objects.filter(
            is_active=True
        )

        if supplier_id:
            suppliers = suppliers.filter(
                id=supplier_id
            )

        results = []

        total_purchase = Decimal("0.00")
        total_paid = Decimal("0.00")
        total_balance = Decimal("0.00")

        for supplier in suppliers:

            purchases = PurchaseInvoice.objects.filter(
                supplier=supplier
            ).aggregate(
                total=Coalesce(
                    Sum("grand_total"),
                    Decimal("0.00")
                )
            )["total"]

            paid = SupplierPayment.objects.filter(
                supplier=supplier
            ).aggregate(
                total=Coalesce(
                    Sum("amount"),
                    Decimal("0.00")
                )
            )["total"]

            balance = supplier.current_balance

            total_purchase += purchases
            total_paid += paid
            total_balance += balance

            results.append({

                "supplier": supplier.name,

                "purchases": purchases,

                "paid": paid,

                "balance": balance,

            })

        return Response({

            "summary": {

                "suppliers": len(results),

                "purchases": total_purchase,

                "paid": total_paid,

                "balance": total_balance,

            },

            "results": results,

        })
    
# ==========================================================
# OUTSTANDING CUSTOMERS REPORT
# ==========================================================

class OutstandingCustomersView(APIView):

    def get(self, request):

        customers = (
            Customer.objects
            .filter(
                current_balance__gt=0,
                is_active=True,
            )
            .order_by("-current_balance")
        )

        results = []

        total_outstanding = Decimal("0.00")

        for customer in customers:

            total_outstanding += customer.current_balance

            results.append({

                "customer": customer.name,

                "mobile": customer.mobile,

                "city": customer.city,

                "balance": customer.current_balance,

            })

        return Response({

            "summary": {

                "customers": len(results),

                "outstanding": total_outstanding,

            },

            "results": results,

        })


# ==========================================================
# OUTSTANDING SUPPLIERS REPORT
# ==========================================================

class OutstandingSuppliersView(APIView):

    def get(self, request):

        suppliers = (
            Supplier.objects
            .filter(
                current_balance__gt=0,
                is_active=True,
            )
            .order_by("-current_balance")
        )

        results = []

        total_outstanding = Decimal("0.00")

        for supplier in suppliers:

            total_outstanding += supplier.current_balance

            results.append({

                "supplier": supplier.name,

                "mobile": supplier.mobile,

                "city": supplier.city,

                "balance": supplier.current_balance,

            })

        return Response({

            "summary": {

                "suppliers": len(results),

                "outstanding": total_outstanding,

            },

            "results": results,

        })


# ==========================================================
# STOCK REPORT
# ==========================================================

class StockReportView(APIView):

    def get(self, request):

        products = (
            Product.objects
            .select_related("category")
            .filter(is_active=True)
            .order_by("product_name")
        )

        results = []

        total_stock = 0

        total_stock_value = Decimal("0.00")

        for product in products:

            stock_value = (
                Decimal(product.current_stock)
                * product.purchase_price
            )

            total_stock += product.current_stock

            total_stock_value += stock_value

            results.append({

                "product": product.product_name,

                "category": product.category.name,

                "stock": product.current_stock,

                "unit": product.unit,

                "purchase_price": product.purchase_price,

                "selling_price": product.default_selling_price,

                "stock_value": stock_value,

            })

        return Response({

            "summary": {

                "products": len(results),

                "stock": total_stock,

                "inventory_value": total_stock_value,

            },

            "results": results,

        })

# ==========================================================
# PROFIT REPORT
# ==========================================================


class ProfitReportView(APIView):

    def get(self, request):

        today = timezone.localdate()

        period = request.GET.get("period", "month")

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")

        items = SalesInvoiceItem.objects.select_related(
            "invoice",
            "product",
            "invoice__customer",
        )

        # -----------------------------------------
        # Date Filter
        # -----------------------------------------

        if from_date and to_date:

            items = items.filter(
                invoice__invoice_date__range=[
                    from_date,
                    to_date,
                ]
            )

        elif period.isdigit():

            items = items.filter(
                invoice__invoice_date__year=today.year,
                invoice__invoice_date__month=int(period),
            )

        elif period == "year":

            items = items.filter(
                invoice__invoice_date__year=today.year,
            )

        elif period == "last_month":

            first_day = today.replace(day=1)

            last_month = first_day - timedelta(days=1)

            items = items.filter(
                invoice__invoice_date__year=last_month.year,
                invoice__invoice_date__month=last_month.month,
            )

        else:

            # Default = current month

            items = items.filter(
                invoice__invoice_date__year=today.year,
                invoice__invoice_date__month=today.month,
            )

        # -----------------------------------------
        # Summary
        # -----------------------------------------

        summary = items.aggregate(

            total_profit=Coalesce(
                Sum("profit"),
                Decimal("0.00"),
            ),

            total_sales=Coalesce(
                Sum("total"),
                Decimal("0.00"),
            ),

            total_items=Count("id"),

        )

        # -----------------------------------------
        # Customer Wise Profit
        # -----------------------------------------

        customer_profit = (
            items
            .values(
                "invoice__customer_id",
                "invoice__customer__name",
            )
            .annotate(

                sales=Coalesce(
                    Sum("total"),
                    Decimal("0.00"),
                ),

                profit=Coalesce(
                    Sum("profit"),
                    Decimal("0.00"),
                ),

                items=Count("id"),

            )
            .order_by("-profit")
        )

        results = []

        for row in customer_profit:

            results.append({

                "customer_id":
                    row["invoice__customer_id"],

                "customer":
                    row["invoice__customer__name"],

                "sales":
                    row["sales"],

                "profit":
                    row["profit"],

                "items":
                    row["items"],

            })

        return Response({

            "summary": summary,

            "results": results,

        })
# ==========================================================
# INVENTORY VALUATION REPORT
# ==========================================================

class InventoryValuationView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            is_active=True
        )

        results = []

        purchase_total = Decimal("0.00")

        selling_total = Decimal("0.00")

        expected_profit = Decimal("0.00")

        for product in products:

            purchase_value = (
                Decimal(product.current_stock)
                * product.purchase_price
            )

            selling_value = (
                Decimal(product.current_stock)
                * product.default_selling_price
            )

            profit = (
                selling_value
                - purchase_value
            )

            purchase_total += purchase_value

            selling_total += selling_value

            expected_profit += profit

            results.append({

                "product": product.product_name,

                "stock": product.current_stock,

                "purchase_value": purchase_value,

                "selling_value": selling_value,

                "expected_profit": profit,

            })

        return Response({

            "summary": {

                "purchase_value": purchase_total,

                "selling_value": selling_total,

                "expected_profit": expected_profit,

            },

            "results": results,

        })


# ==========================================================
# LOW STOCK REPORT
# ==========================================================

class LowStockReportView(APIView):

    LOW_STOCK_LIMIT = 10

    def get(self, request):

        products = (
            Product.objects
            .filter(
                current_stock__lte=self.LOW_STOCK_LIMIT,
                is_active=True,
            )
            .order_by(
                "current_stock",
                "product_name",
            )
        )

        results = []

        for product in products:

            results.append({

                "product": product.product_name,

                "category": product.category.name,

                "stock": product.current_stock,

                "unit": product.unit,

                "purchase_price": product.purchase_price,

                "selling_price": product.default_selling_price,

            })

        return Response({

            "summary": {

                "low_stock_products": len(results),

            },

            "results": results,

        })
    
# ==========================================================
# MONTHLY SALES REPORT
# ==========================================================




class MonthlySalesReportView(APIView):

    def get(self, request):

        monthly = (
            SalesInvoice.objects
            .annotate(month=TruncMonth("invoice_date"))
            .values("month")
            .annotate(
                sales=Coalesce(
                    Sum("grand_total"),
                    Decimal("0.00"),
                ),
                invoices=Count("id"),
            )
            .order_by("month")
        )

        data = {
            row["month"].strftime("%b"): {
                "sales": float(row["sales"]),
                "invoices": row["invoices"],
            }
            for row in monthly
        }

        month_map = {
          "Jan": "jan",
          "Feb": "feb",
          "Mar": "mar",
          "Apr": "apr",
          "May": "may",
          "Jun": "jun",
          "Jul": "jul",
          "Aug": "aug",
          "Sep": "sep",
          "Oct": "oct",
          "Nov": "nov",
          "Dec": "dec",
}

        results = []

        total_sales = 0

        for month in month_map:

         sales = data.get(month, {}).get("sales", 0)

         invoices = data.get(month, {}).get("invoices", 0)

         total_sales += sales

         results.append({
          "month": month,
          "period": month_map[month],   # <-- add this
          "sales": sales,
          "invoices": invoices,
         })
        return Response({

            "summary": {
                "months": 12,
                "total_sales": total_sales,
            },

            "results": results,

        })


# ==========================================================
# MONTHLY PROFIT REPORT
# ==========================================================



class MonthlyProfitReportView(APIView):

    def get(self, request):

        monthly = (
            SalesInvoice.objects
            .annotate(
                month=TruncMonth("invoice_date")
            )
            .values("month")
            .annotate(
                profit=Coalesce(
                    Sum("total_profit"),
                    Decimal("0.00"),
                ),
                invoices=Count("id"),
            )
            .order_by("month")
        )

        data = {
              row["month"].strftime("%b").lower(): {
                "profit": float(row["profit"]),
                "invoices": row["invoices"],
            }
            for row in monthly
        }

        month_map = {
          "jan": 1,
          "feb": 2,
          "mar": 3,
          "apr": 4,
          "may": 5,
          "jun": 6,
          "jul": 7,
          "aug": 8,
          "sep": 9,
          "oct": 10,
          "nov": 11,
          "dec": 12,
        }

        results = []

        total_profit = 0
 
        for month in month_map:

         profit = data.get(month, {}).get("profit", 0)

         invoices = data.get(month, {}).get("invoices", 0)

         total_profit += profit

         results.append({
          "month": month,
          "period": str(month_map[month]),  # <-- add this
          "profit": profit,
          "invoices": invoices,
        })
        return Response({

            "summary": {

                "months": 12,

                "total_profit": total_profit,

            },

            "results": results,

        })


# ==========================================================
# PROFIT SUMMARY REPORT
# ==========================================================

class ProfitSummaryView(APIView):

    def get(self, request):

        sales = SalesInvoice.objects.aggregate(

            total_sales=Coalesce(
                Sum("grand_total"),
                Decimal("0.00")
            ),

            total_profit=Coalesce(
                Sum("total_profit"),
                Decimal("0.00")
            ),

        )

        purchases = PurchaseInvoice.objects.aggregate(

            total_purchase=Coalesce(
                Sum("grand_total"),
                Decimal("0.00")
            )

        )

        inventory = Product.objects.aggregate(

            inventory_value=Coalesce(

                Sum(
                    ExpressionWrapper(
                        F("current_stock") * F("purchase_price"),
                        output_field=DecimalField(
                            max_digits=15,
                            decimal_places=2
                        ),
                    )
                ),

                Decimal("0.00")

            )

        )

        return Response({

            "summary": {

                "total_sales":
                    sales["total_sales"],

                "total_purchase":
                    purchases["total_purchase"],

                "total_profit":
                    sales["total_profit"],

                "inventory_value":
                    inventory["inventory_value"],

            }

        })


# ==========================================================
# TOP CUSTOMERS REPORT
# ==========================================================

class TopCustomersView(APIView):

    def get(self, request):

        customers = (
            SalesInvoice.objects
            .values(
                "customer",
                "customer__name",
            )
            .annotate(
                sales=Coalesce(
                    Sum("grand_total"),
                    Decimal("0.00")
                ),
                profit=Coalesce(
                    Sum("total_profit"),
                    Decimal("0.00")
                ),
                invoices=Count("id"),
            )
            .order_by("-sales")[:10]
        )

        return Response({

            "summary": {

                "customers": customers.count(),

            },

            "results": customers,

        })


# ==========================================================
# TOP PRODUCTS REPORT
# ==========================================================

class TopProductsView(APIView):

    def get(self, request):

        products = (
            SalesInvoiceItem.objects
            .values(
                "product",
                "product__product_name",
            )
            .annotate(
                quantity=Coalesce(
                    Sum("quantity"),
                    0,
                ),
                sales=Coalesce(
                    Sum("total"),
                    Decimal("0.00")
                ),
                profit=Coalesce(
                    Sum("profit"),
                    Decimal("0.00")
                ),
            )
            .order_by("-sales")[:10]
        )

        return Response({

            "summary": {

                "products": products.count(),

            },

            "results": products,

        })
    



class SalesExcelExportView(APIView):

    def get(self, request):
        return export_sales_excel()


class PurchaseExcelExportView(APIView):

    def get(self, request):
        return export_purchase_excel()


class StockExcelExportView(APIView):

    def get(self, request):
        return export_stock_excel()


class CustomerLedgerExcelExportView(APIView):

    def get(self, request):
        return export_customer_ledger_excel()


class SupplierLedgerExcelExportView(APIView):

    def get(self, request):
        return export_supplier_ledger_excel()


class ProfitExcelExportView(APIView):

    def get(self, request):
        return export_profit_excel()


class CustomerSalesExcelExportView(APIView):

    def get(self, request):
        return export_customer_sales_excel()


class ProductSalesExcelExportView(APIView):

    def get(self, request):
        return export_product_sales_excel()

class SalesAnalyticsView(APIView):

    def get(self, request):
        

        today = timezone.localdate()

        period = request.GET.get("period", "month")

        if period == "year":

          sales_queryset = SalesInvoice.objects.filter(
           invoice_date__year=today.year,
         )

        elif period == "last_month":

         first_day = today.replace(day=1)

         last_month = first_day - timedelta(days=1)

         sales_queryset = SalesInvoice.objects.filter(
          invoice_date__year=last_month.year,
          invoice_date__month=last_month.month,
         )

        else:

         sales_queryset = SalesInvoice.objects.filter(
          invoice_date__year=today.year,
          invoice_date__month=today.month,
        )
        # -----------------------------
        # Monthly Sales
        # -----------------------------
        monthly_sales = (
            sales_queryset
            .annotate(month=TruncMonth("invoice_date"))
            .values("month")
            .annotate(
                sales=Coalesce(
                    Sum("grand_total"),
                    Decimal("0.00"),
                ),
            )
            .order_by("month")
        )

        monthly_sales_data = []

        for row in monthly_sales:
          monthly_sales_data.append({
           "month": row["month"].strftime("%b") if row["month"] else "",
           "sales": float(row["sales"]),
        })

        # -----------------------------
        # Monthly Profit
        # -----------------------------
        monthly_profit = (
            SalesInvoiceItem.objects.filter(
    invoice__in=sales_queryset
)
            .annotate(
                month=TruncMonth("invoice__invoice_date")
            )
            .values("month")
            .annotate(
                profit=Coalesce(
                    Sum("profit"),
                    Decimal("0.00"),
                ),
            )
            .order_by("month")
        )

        monthly_profit_data = []

        for row in monthly_profit:
         monthly_profit_data.append({
          "month": row["month"].strftime("%b") if row["month"] else "",
          "profit": float(row["profit"]),
        })

        # -----------------------------
        # Top Customers
        # -----------------------------
        top_customers = (
            sales_queryset
            .values("customer__name")
            .annotate(
                total=Sum("grand_total"),
            )
            .order_by("-total")[:10]
        )

        customer_data = []

        for row in top_customers:
            customer_data.append({
                "name": row["customer__name"],
                "amount": float(row["total"]),
            })

        # -----------------------------
        # Top Products
        # -----------------------------
        top_products = (
            SalesInvoiceItem.objects.filter(
    invoice__in=sales_queryset
)
            .values("product__product_name")
            .annotate(
                qty=Sum("quantity"),
            )
            .order_by("-qty")[:10]
        )

        product_data = []

        for row in top_products:
            product_data.append({
                "name": row["product__product_name"],
                "qty": row["qty"],
            })

        # -----------------------------
        # Summary
        # -----------------------------
        summary = {

            "total_sales":

                sales_queryset.aggregate(

                    total=Coalesce(
                        Sum("grand_total"),
                        Decimal("0.00"),
                    )

                )["total"],

            "total_profit":

                SalesInvoiceItem.objects.filter(
    invoice__in=sales_queryset
).aggregate(

                    total=Coalesce(
                        Sum("profit"),
                        Decimal("0.00"),
                    )

                )["total"],

            "invoice_count":
                sales_queryset.count(),

            "average_invoice":

                sales_queryset.aggregate(

                    avg=Coalesce(
                        Avg("grand_total"),
                        Decimal("0.00"),
                    )

                )["avg"],

        }
        # -----------------------------
# Sales Overview (Last 6 Months)
# -----------------------------

        start_month = today.replace(day=1) - relativedelta(months=5)

        overview_sales = (
          SalesInvoice.objects
          .filter(invoice_date__gte=start_month)
          .annotate(month=TruncMonth("invoice_date"))
          .values("month")
          .annotate(
              total=Coalesce(
                Sum("grand_total"),
                Decimal("0.00"),
              ),
            )
            .order_by("month")
        )

        sales_chart = []

        for row in overview_sales:
          sales_chart.append({
            "month": row["month"].strftime("%b"),
            "value": float(row["total"]),
          })

        current_sales = sales_chart[-1]["value"] if sales_chart else 0
        previous_sales = sales_chart[-2]["value"] if len(sales_chart) > 1 else 0

        sales_growth = 0

        if previous_sales > 0:
          sales_growth = (
           (current_sales - previous_sales)
           / previous_sales
          ) * 100


# -----------------------------
# Profit Overview (Last 6 Months)
# -----------------------------

        overview_profit = (
        SalesInvoiceItem.objects
        .filter(
          invoice__invoice_date__gte=start_month
        )
        .annotate(
         month=TruncMonth("invoice__invoice_date")
        )
        .values("month")
        .annotate(
         total=Coalesce(
            Sum("profit"),
            Decimal("0.00"),
         ),
        )
         .order_by("month")
        )

        profit_chart = []

        for row in overview_profit:
         profit_chart.append({
           "month": row["month"].strftime("%b"),
           "value": float(row["total"]),
         })

        current_profit = profit_chart[-1]["value"] if profit_chart else 0
        previous_profit = profit_chart[-2]["value"] if len(profit_chart) > 1 else 0

        profit_growth = 0

        if previous_profit > 0:
         profit_growth = (
          (current_profit - previous_profit)
          / previous_profit
         ) * 100

        return Response({

         "summary": summary,

         "monthly_sales": monthly_sales_data,

         "monthly_profit": monthly_profit_data,

         "top_products": product_data,

         "top_customers": customer_data,

    
         "sales_overview": {
          "current_month": today.strftime("%b"),
          "current_total": current_sales,
          "previous_total": previous_sales,
          "growth": round(sales_growth, 2),
          "chart": sales_chart,
         },

        # NEW
        "profit_overview": {
          "current_month": today.strftime("%b"),
          "current_total": current_profit,
          "previous_total": previous_profit,
          "growth": round(profit_growth, 2),
          "chart": profit_chart,
    },

})