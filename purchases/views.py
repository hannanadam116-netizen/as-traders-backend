from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.generics import get_object_or_404
from django.utils import timezone
from .pdf import generate_purchase_invoice
from django.utils import timezone
from datetime import timedelta
from .models import PurchaseInvoice
from .serializers import (
    CreatePurchaseInvoiceSerializer,
    PurchaseInvoiceSerializer,
)
from .services import PurchaseService


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

      invoices = PurchaseInvoice.objects.prefetch_related(
        "items"
      ).select_related(
        "supplier"
      )

    # ----------------------------
    # Date Filters
    # ----------------------------

      if filter_type == "today":

        invoices = invoices.filter(
            invoice_date=today,
        )

      elif filter_type == "yesterday":

        invoices = invoices.filter(
            invoice_date=today - timedelta(days=1),
        )

      elif filter_type == "this_week":

        start = today - timedelta(days=today.weekday())

        invoices = invoices.filter(
            invoice_date__gte=start,
        )

      elif filter_type == "this_month":

        invoices = invoices.filter(
            invoice_date__year=today.year,
            invoice_date__month=today.month,
        )

      if from_date:

        invoices = invoices.filter(
            invoice_date__gte=from_date,
        )

      if to_date:

        invoices = invoices.filter(
            invoice_date__lte=to_date,
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
            "-grand_total",
        )

      elif sort == "lowest":

        invoices = invoices.order_by(
            "grand_total",
        )

      elif sort == "supplier":

        invoices = invoices.order_by(
            "supplier__name",
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

        serializer.is_valid(raise_exception=True)

        invoice = PurchaseService.create_purchase_invoice(
            serializer.validated_data
        )

        output = PurchaseInvoiceSerializer(invoice)

        return Response(
            output.data,
            status=status.HTTP_201_CREATED
        )
class TodayPurchaseListView(APIView):

    def get(self, request):

        today = timezone.localdate()

        invoices = (
            PurchaseInvoice.objects
            .filter(invoice_date=today)
            .select_related("supplier")
            .prefetch_related("items")
        )

        serializer = PurchaseInvoiceSerializer(
            invoices,
            many=True,
        )

        return Response(serializer.data)

class PurchaseInvoiceDetailView(APIView):
    """
    GET    : Purchase Invoice Details
    PUT    : Update Purchase Invoice
    DELETE : Delete Purchase Invoice
    """

    def get(self, request, pk):

        invoice = PurchaseInvoice.objects.prefetch_related(
            "items"
        ).select_related(
            "supplier"
        ).get(pk=pk)

        serializer = PurchaseInvoiceSerializer(
            invoice,
        )

        return Response(
            serializer.data,
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

        return Response(
            PurchaseInvoiceSerializer(
                invoice,
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
            .prefetch_related("items__product"),
            pk=pk,
        )

        return generate_purchase_invoice(invoice)