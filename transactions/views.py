from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from datetime import timedelta
from .pdf import generate_sales_invoice
from .models import SalesInvoice

from .models import SalesInvoice
from .serializers import (
    CreateInvoiceSerializer,
    SalesInvoiceSerializer,
)
from .services import SalesService


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

        invoices = SalesInvoice.objects.prefetch_related(
         "items"
        ).select_related(
          "customer"
        )

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
        sort = request.GET.get("sort")

        if sort == "oldest":
         invoices = invoices.order_by("invoice_date", "id")

        elif sort == "highest":
          invoices = invoices.order_by("-grand_total")

        elif sort == "lowest":
         invoices = invoices.order_by("grand_total")

        elif sort == "customer":
          invoices = invoices.order_by("customer__name")

        else:
         invoices = invoices.order_by("-invoice_date", "-id")

        serializer = SalesInvoiceSerializer(
            invoices,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = CreateInvoiceSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        invoice = SalesService.create_invoice(
            serializer.validated_data
        )

        output = SalesInvoiceSerializer(invoice)

        return Response(
            output.data,
            status=status.HTTP_201_CREATED
        )


class SalesInvoiceDetailView(APIView):
    """
    GET     : Invoice Details
    PUT     : Update Invoice
    DELETE  : Delete Invoice
    """

    def get(self, request, pk):

        invoice = get_object_or_404(
            SalesInvoice.objects
            .select_related("customer")
            .prefetch_related("items"),
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
            SalesInvoice.objects
            .filter(invoice_date=today)
            .prefetch_related("items")
            .select_related("customer")
        )

        serializer = SalesInvoiceSerializer(
            invoices,
            many=True,
        )

        return Response(serializer.data)



class SalesInvoicePDFView(APIView):

    def get(self, request, pk):

        invoice = get_object_or_404(
            SalesInvoice.objects.prefetch_related(
                "items__product"
            ).select_related(
                "customer"
            ),
            pk=pk,
        )

        return generate_sales_invoice(invoice)