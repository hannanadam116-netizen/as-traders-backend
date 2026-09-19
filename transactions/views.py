from datetime import timedelta

from django.db.models import Prefetch
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SalesInvoice, SalesInvoiceItem
from .pdf import generate_sales_invoice
from .serializers import (
    CreateInvoiceSerializer,
    SalesInvoiceSerializer,
)
from .services import SalesService


def invoice_queryset():
    """
    Optimized invoice queryset.

    Loads:
    - customer with the invoice
    - products with the invoice items

    This prevents extra database queries while serializing invoices.
    """
    items_queryset = SalesInvoiceItem.objects.select_related("product")

    return (
        SalesInvoice.objects
        .select_related("customer")
        .prefetch_related(
            Prefetch(
                "items",
                queryset=items_queryset,
            )
        )
    )


class SalesInvoiceListCreateView(APIView):
    """
    GET  : List all invoices
    POST : Create new invoice
    """

    def get(self, request):
        today = timezone.localdate()

        from_date = request.GET.get("from")
        to_date = request.GET.get("to")
        filter_type = request.GET.get("filter")

        invoices = invoice_queryset()

        if filter_type == "today":
            invoices = invoices.filter(
                invoice_date=today
            )

        elif filter_type == "yesterday":
            invoices = invoices.filter(
                invoice_date=today - timedelta(days=1)
            )

        elif filter_type == "this_week":
            start = today - timedelta(days=today.weekday())

            invoices = invoices.filter(
                invoice_date__gte=start
            )

        elif filter_type == "this_month":
            invoices = invoices.filter(
                invoice_date__year=today.year,
                invoice_date__month=today.month,
            )

        if from_date:
            invoices = invoices.filter(
                invoice_date__gte=from_date
            )

        if to_date:
            invoices = invoices.filter(
                invoice_date__lte=to_date
            )

        sort = request.GET.get("sort")

        if sort == "oldest":
            invoices = invoices.order_by(
                "invoice_date",
                "id",
            )

        elif sort == "highest":
            invoices = invoices.order_by(
                "-grand_total"
            )

        elif sort == "lowest":
            invoices = invoices.order_by(
                "grand_total"
            )

        elif sort == "customer":
            invoices = invoices.order_by(
                "customer__name"
            )

        else:
            invoices = invoices.order_by(
                "-invoice_date",
                "-id",
            )

        serializer = SalesInvoiceSerializer(
            invoices,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = CreateInvoiceSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        invoice = SalesService.create_invoice(
            serializer.validated_data
        )

        output = SalesInvoiceSerializer(
            invoice
        )

        return Response(
            output.data,
            status=status.HTTP_201_CREATED,
        )


class SalesInvoiceDetailView(APIView):
    """
    GET     : Invoice Details
    PUT     : Update Invoice
    DELETE  : Delete Invoice
    """

    def get(self, request, pk):
        invoice = get_object_or_404(
            invoice_queryset(),
            pk=pk,
        )

        serializer = SalesInvoiceSerializer(
            invoice
        )

        return Response(
            serializer.data
        )

    def put(self, request, pk):
        invoice = get_object_or_404(
            SalesInvoice,
            pk=pk,
        )

        serializer = CreateInvoiceSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        invoice = SalesService.update_invoice(
            invoice,
            serializer.validated_data,
        )

        output = SalesInvoiceSerializer(
            invoice
        )

        return Response(
            output.data
        )

    def delete(self, request, pk):
        invoice = get_object_or_404(
            SalesInvoice,
            pk=pk,
        )

        SalesService.delete_invoice(
            invoice
        )

        return Response(
            {
                "message":
                "Invoice deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class TodaySalesListView(APIView):

    def get(self, request):
        today = timezone.localdate()

        invoices = (
            invoice_queryset()
            .filter(invoice_date=today)
        )

        serializer = SalesInvoiceSerializer(
            invoices,
            many=True,
        )

        return Response(serializer.data)


class SalesInvoicePDFView(APIView):

    def get(self, request, pk):
        invoice = get_object_or_404(
            SalesInvoice.objects
            .select_related("customer")
            .prefetch_related(
                Prefetch(
                    "items",
                    queryset=SalesInvoiceItem.objects.select_related(
                        "product"
                    ),
                )
            ),
            pk=pk,
        )

        return generate_sales_invoice(invoice)