from decimal import Decimal

from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView

from masters.models import Product, Customer, Supplier
from transactions.models import SalesInvoice
from purchases.models import PurchaseInvoice
from payments.models import CustomerPayment, SupplierPayment
from transactions.serializers import SalesInvoiceSerializer
from purchases.serializers import PurchaseInvoiceSerializer


class DashboardSummaryView(APIView):

    def get(self, request):

        today = timezone.localdate()

        today_sales = SalesInvoice.objects.filter(
            invoice_date=today
        ).aggregate(
            total=Coalesce(
                Sum("grand_total"),
                Decimal("0.00"),
            )
        )["total"]

        today_purchases = PurchaseInvoice.objects.filter(
            invoice_date=today
        ).aggregate(
            total=Coalesce(
                Sum("grand_total"),
                Decimal("0.00"),
            )
        )["total"]

        today_collections = CustomerPayment.objects.filter(
            payment_date=today
        ).aggregate(
            total=Coalesce(
                Sum("amount"),
                Decimal("0.00"),
            )
        )["total"]

        today_supplier_payments = SupplierPayment.objects.filter(
            payment_date=today
        ).aggregate(
            total=Coalesce(
                Sum("amount"),
                Decimal("0.00"),
            )
        )["total"]

        customer_outstanding = Customer.objects.aggregate(
            total=Coalesce(
                Sum("current_balance"),
                Decimal("0.00"),
            )
        )["total"]

        supplier_outstanding = Supplier.objects.aggregate(
            total=Coalesce(
                Sum("current_balance"),
                Decimal("0.00"),
            )
        )["total"]

        total_products = Product.objects.count()

        stock_value = Product.objects.aggregate(
            total=Coalesce(
                Sum(
                    F("current_stock") *
                    F("purchase_price")
                ),
                Decimal("0.00"),
            )
        )["total"]
        monthly_sales = SalesInvoice.objects.filter(
          invoice_date__year=today.year,
          invoice_date__month=today.month,
        ).aggregate(
         total=Coalesce(
          Sum("grand_total"),
          Decimal("0.00"),
         )
        )["total"]

        monthly_profit = SalesInvoice.objects.filter(
         invoice_date__year=today.year,
         invoice_date__month=today.month,
        ).aggregate(
           total=Coalesce(
             Sum("total_profit"),
             Decimal("0.00"),
            )
        )["total"]

        recent_sales = []

        for invoice in (
            SalesInvoice.objects
            .select_related("customer")
            .order_by("-invoice_number")[:10]
        ):

            recent_sales.append({
                "invoice_number": invoice.display_invoice_number,
                "customer": invoice.customer.name,
                "grand_total": invoice.grand_total,
                "date": invoice.invoice_date,
            })

        recent_purchases = []

        for invoice in (
            PurchaseInvoice.objects
            .select_related("supplier")
            .order_by("-invoice_number")[:10]
        ):

            recent_purchases.append({
                "invoice_number": invoice.display_invoice_number,
                "supplier": invoice.supplier.name,
                "grand_total": invoice.grand_total,
                "date": invoice.invoice_date,
            })

        low_stock = []

        for product in (
            Product.objects
            .filter(current_stock__lte=10)
            .order_by(
                "current_stock",
                "product_name",
            )[:3]
        ):

            low_stock.append({
                "id": product.id,
                "product_name": product.product_name,
                "category": product.category.name,
                "stock": product.current_stock,
                "unit": product.unit,
                "purchase_price": product.purchase_price,
                "selling_price": product.default_selling_price,
            })

        return Response({

            "today_sales": today_sales,
            "today_purchases": today_purchases,
            "monthly_sales": monthly_sales,
            "monthly_profit": monthly_profit,
            "today_collections": today_collections,
            "today_supplier_payments": today_supplier_payments,
            "customer_outstanding": customer_outstanding,
            "supplier_outstanding": supplier_outstanding,
            "total_products": total_products,
            "stock_value": stock_value,

            "recent_sales": recent_sales,
            "recent_purchases": recent_purchases,
            "low_stock": low_stock,

        })
class TodaySalesView(APIView):

    def get(self, request):

        today = timezone.localdate()

        invoices = (
            SalesInvoice.objects
            .select_related("customer")
            .filter(invoice_date=today)
            .order_by("-invoice_number")
        )

        data = []

        for invoice in invoices:
            data.append({
                "id": invoice.id,
                "invoice_number": invoice.display_invoice_number,
                "party_name": invoice.customer.name,
                "grand_total": invoice.grand_total,
                "date": invoice.invoice_date,
            })

        return Response(data)


class TodayPurchasesView(APIView):

    def get(self, request):

        today = timezone.localdate()

        invoices = (
            PurchaseInvoice.objects
            .select_related("supplier")
            .filter(invoice_date=today)
            .order_by("-invoice_number")
        )

        data = []

        for invoice in invoices:
            data.append({
                "id": invoice.id,
                "invoice_number": invoice.display_invoice_number,
                "party_name": invoice.supplier.name,
                "grand_total": invoice.grand_total,
                "date": invoice.invoice_date,
            })

        return Response(data)


class CustomerOutstandingView(APIView):

    def get(self, request):

        customers = (
            Customer.objects
            .filter(current_balance__gt=0)
            .order_by("-current_balance")
        )

        data = []

        for customer in customers:
            data.append({
                "id": customer.id,
                "name": customer.name,
                "balance": customer.current_balance,
            })

        return Response(data)


class SupplierOutstandingView(APIView):

    def get(self, request):

        suppliers = (
            Supplier.objects
            .filter(current_balance__gt=0)
            .order_by("-current_balance")
        )

        data = []

        for supplier in suppliers:
            data.append({
                "id": supplier.id,
                "name": supplier.name,
                "balance": supplier.current_balance,
            })

        return Response(data)