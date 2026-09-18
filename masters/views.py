from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import MastersService
from .models import (
    Product,
    Customer,
    Supplier,
    CustomerProductPrice,

)

from .serializers import (
    CustomerSerializer,
    SupplierSerializer,
    CustomerProductPriceSerializer,
)
# ==========================================
# CATEGORY
# ==========================================

class CategoryListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            MastersService.get_categories()

        )

    def post(self, request):

        return Response(

            MastersService.create_category(
                request.data
            ),

            status=status.HTTP_201_CREATED,

        )


# ==========================================
# PRODUCT LIST / CREATE
# ==========================================

class ProductListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(

            MastersService.get_products()

        )

    def post(self, request):

        return Response(

            MastersService.create_product(
                request.data
            ),

            status=status.HTTP_201_CREATED,

        )



# ==========================================
# PRODUCT UPDATE / DELETE
# ==========================================

class ProductDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        product = get_object_or_404(

            Product,

            pk=pk,

        )

        return Response(

            MastersService.update_product(

                product,

                request.data,

            )

        )

    def delete(self, request, pk):

        product = get_object_or_404(

            Product,

            pk=pk,

        )

        return Response(

            MastersService.delete_product(

                product

            )

        )


# ==========================================
# CUSTOMER
# ==========================================
class CustomerListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            MastersService.get_customers()
        )

    def post(self, request):
        return Response(
            MastersService.create_customer(
                request.data
            ),
            status=status.HTTP_201_CREATED,
        )
    
class CustomerDetailView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, pk):

        customer = get_object_or_404(
            Customer,
            pk=pk,
        )

        serializer = CustomerSerializer(
            customer,
        )

        return Response(
            serializer.data,
        )

    def put(self, request, pk):

        customer = get_object_or_404(
            Customer,
            pk=pk,
        )

        return Response(
            MastersService.update_customer(
                customer,
                request.data,
            )
        )

    def delete(self, request, pk):

        customer = get_object_or_404(
            Customer,
            pk=pk,
        )

        return Response(
            MastersService.delete_customer(
                customer,
            )
        )

# ==========================================
# SUPPLIER
# ==========================================

class SupplierListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(
            MastersService.get_suppliers()
        )

    def post(self, request):

        return Response(
            MastersService.create_supplier(
                request.data
            ),
            status=status.HTTP_201_CREATED,
        )


class SupplierDetailView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, pk):

      supplier = get_object_or_404(
        Supplier,
        pk=pk,
      )

      serializer = SupplierSerializer(
        supplier,
      )

      return Response(
        serializer.data,
      )
    def put(self, request, pk):

        supplier = get_object_or_404(
            Supplier,
            pk=pk,
        )

        return Response(
            MastersService.update_supplier(
                supplier,
                request.data,
            )
        )

    def delete(self, request, pk):

        supplier = get_object_or_404(
            Supplier,
            pk=pk,
        )

        return Response(
            MastersService.delete_supplier(
                supplier,
            )
        )
class OutstandingCustomerListView(APIView):

    def get(self, request):

        customers = Customer.objects.filter(
            current_balance__gt=0
        ).order_by("-current_balance")

        serializer = CustomerSerializer(
            customers,
            many=True,
        )

        return Response(serializer.data)
class OutstandingSupplierListView(APIView):

    def get(self, request):

        suppliers = (
            Supplier.objects
            .filter(current_balance__gt=0)
            .order_by("-current_balance")
        )

        serializer = SupplierSerializer(
            suppliers,
            many=True,
        )

        return Response(serializer.data)

# ==========================================
# CUSTOMER PRODUCT PRICE
# ==========================================

class CustomerProductPriceListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        customer = request.query_params.get("customer")

        queryset = CustomerProductPrice.objects.select_related(
            "customer",
            "product",
        )

        if customer:
            queryset = queryset.filter(customer_id=customer)

        serializer = CustomerProductPriceSerializer(
            queryset,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = CustomerProductPriceSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CustomerProductPriceDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        price = get_object_or_404(
            CustomerProductPrice,
            pk=pk,
        )

        serializer = CustomerProductPriceSerializer(
            price,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):

        price = get_object_or_404(
            CustomerProductPrice,
            pk=pk,
        )

        price.delete()

        return Response(
            {"message": "Deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )