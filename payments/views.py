from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    CustomerPayment,
    SupplierPayment,
)

from .serializers import (
    CustomerPaymentSerializer,
    SupplierPaymentSerializer,
    CreateCustomerPaymentSerializer,
    CreateSupplierPaymentSerializer,
)

from .services import (
    CustomerPaymentService,
    SupplierPaymentService,
)


# ==========================================================
# CUSTOMER PAYMENT
# ==========================================================

class CustomerPaymentListCreateView(APIView):

    def get(self, request):

        payments = CustomerPayment.objects.select_related(
            "customer"
        )

        serializer = CustomerPaymentSerializer(
            payments,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = CreateCustomerPaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        payment = CustomerPaymentService.create_payment(
            serializer.validated_data
        )

        output = CustomerPaymentSerializer(
            payment
        )

        return Response(
            output.data,
            status=status.HTTP_201_CREATED,
        )


class CustomerPaymentDetailView(APIView):

    def get(self, request, pk):

        payment = CustomerPayment.objects.select_related(
            "customer"
        ).get(pk=pk)

        serializer = CustomerPaymentSerializer(
            payment
        )

        return Response(serializer.data)
    def delete(self, request, pk):

      payment = CustomerPayment.objects.get(pk=pk)

      CustomerPaymentService.delete_payment(payment)

      return Response(
        status=status.HTTP_204_NO_CONTENT
    )


# ==========================================================
# SUPPLIER PAYMENT
# ==========================================================

class SupplierPaymentListCreateView(APIView):

    def get(self, request):

        payments = SupplierPayment.objects.select_related(
            "supplier"
        )

        serializer = SupplierPaymentSerializer(
            payments,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = CreateSupplierPaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        payment = SupplierPaymentService.create_payment(
            serializer.validated_data
        )

        output = SupplierPaymentSerializer(
            payment
        )

        return Response(
            output.data,
            status=status.HTTP_201_CREATED,
        )


class SupplierPaymentDetailView(APIView):

    def get(self, request, pk):

        payment = SupplierPayment.objects.select_related(
            "supplier"
        ).get(pk=pk)

        serializer = SupplierPaymentSerializer(
            payment
        )

        return Response(serializer.data)
    
    def delete(self, request, pk):

      payment = SupplierPayment.objects.get(pk=pk)

      SupplierPaymentService.delete_payment(payment)

      return Response(
        status=status.HTTP_204_NO_CONTENT
    )