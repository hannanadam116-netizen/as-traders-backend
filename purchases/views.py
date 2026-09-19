from datetime import timedelta

from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PurchaseInvoice, PurchaseInvoiceItem
from .pdf import generate_purchase_invoice
from .serializers import (
    CreatePurchaseInvoiceSerializer,
    PurchaseInvoiceSerializer,
)
from .services import PurchaseService


def purchase_invoice_queryset():
    """
    Optimized purchase invoice queryset.

    Loads:
    - supplier with the invoice
    - product with every invoice item

    This prevents repeated database queries while
    serializing purchase invoices.
    """

    items_queryset = PurchaseInvoiceItem.objects.select_related(
        "product"
    )

    return (
        PurchaseInvoice.objects
        .select_related("supplier")
        .prefetch_related(
            Prefetch(
                "items",
                queryset=items_queryset,
            )
        )
    )


class PurchaseInvoiceListCreateView(APIView):
    """
    GET  : List Purchase Invoices
    POST : Create Purchase Invoice
    """

    def get(self, request):

        today = timezone.localdate()

        from_date = request.GET.get("from")
        to_date = request.GET.get("to")
        filter_type = request.GET.get("filter")

        invoices = purchase_invoice_queryset()

        # ----------------------------
        # Date Filters
        # ----------------------------

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

        # ----------------------------
        # Sorting
        # ----------------------------

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

        elif sort == "supplier":

            invoices = invoices.order_by(
                "supplier__name"
            )

        else:

            invoices = invoices.order_by(
                "-invoice_date",
                "-id",
            )

        serializer = PurchaseInvoiceSerializer(
            invoices,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = CreatePurchaseInvoiceSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        invoice = PurchaseService.create_purchase_invoice(
            serializer.validated_data
        )

        # Reload the created invoice with related objects
        invoice = purchase_invoice_queryset().get(
            pk=invoice.pk
        )

        output = PurchaseInvoiceSerializer(
            invoice
        )

        return Response(
            output.data,
            status=status.HTTP_201_CREATED,
        )


class TodayPurchaseListView(APIView):

    def get(self, request):

        today = timezone.localdate()

        invoices = (
            purchase_invoice_queryset()
            .filter(invoice_date=today)
            .order_by(
                "-invoice_number"
            )
        )

        serializer = PurchaseInvoiceSerializer(
            invoices,
            many=True,
        )

        return Response(
            serializer.data
        )


class PurchaseInvoiceDetailView(APIView):
    """
    GET    : Purchase Invoice Details
    PUT    : Update Purchase Invoice
    DELETE : Delete Purchase Invoice
    """

    def get(self, request, pk):

        invoice = get_object_or_404(
            purchase_invoice_queryset(),
            pk=pk,
        )

        serializer = PurchaseInvoiceSerializer(
            invoice
        )

        return Response(
            serializer.data
        )

    # ==========================================
    # UPDATE PURCHASE
    # ==========================================

    @transaction.atomic
    def put(self, request, pk):

        invoice = get_object_or_404(
            PurchaseInvoice,
            pk=pk,
        )

        serializer = CreatePurchaseInvoiceSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        invoice = PurchaseService.update_purchase_invoice(
            invoice=invoice,
            data=serializer.validated_data,
        )

        # Reload with related objects
        invoice = purchase_invoice_queryset().get(
            pk=invoice.pk
        )

        return Response(
            PurchaseInvoiceSerializer(
                invoice
            ).data,
        )

    # ==========================================
    # DELETE PURCHASE
    # ==========================================

    @transaction.atomic
    def delete(self, request, pk):

        invoice = get_object_or_404(
            PurchaseInvoice,
            pk=pk,
        )

        PurchaseService.delete_purchase_invoice(
            invoice,
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class PurchaseInvoicePDFView(APIView):

    def get(self, request, pk):

        invoice = get_object_or_404(
            PurchaseInvoice.objects
            .select_related("supplier")
            .prefetch_related(
                Prefetch(
                    "items",
                    queryset=PurchaseInvoiceItem.objects.select_related(
                        "product"
                    ),
                )
            ),
            pk=pk,
        )

        return generate_purchase_invoice(invoice)