from .models import (
    Category,
    Product,
    Customer,
    Supplier,
)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CustomerSerializer,
    SupplierSerializer,
)
from decimal import Decimal

class MastersService:

    # ==========================================
    # CATEGORY
    # ==========================================

    @staticmethod
    def get_categories():

        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories,
            many=True,
        )

        return serializer.data

    @staticmethod
    def create_category(data):

        serializer = CategorySerializer(
            data=data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return serializer.data

    # ==========================================
    # PRODUCT
    # ==========================================

    @staticmethod
    def get_products():

        products = Product.objects.select_related(
            "category"
        )

        serializer = ProductSerializer(
            products,
            many=True,
        )

        return serializer.data

    @staticmethod
    def create_product(data):

        serializer = ProductSerializer(
            data=data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return serializer.data

    @staticmethod
    def update_product(product, data):

        serializer = ProductSerializer(
            product,
            data=data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return serializer.data

    @staticmethod
    def delete_product(product):

        product.delete()

        return {
            "message": "Product deleted successfully."
        }
    # ==========================================
    # CUSTOMER
    # ==========================================

    @staticmethod
    def get_customers():

        customers = Customer.objects.all()

        serializer = CustomerSerializer(
            customers,
            many=True,
        )

        return serializer.data

    @staticmethod
    def create_customer(data):

        serializer = CustomerSerializer(
            data=data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return serializer.data

    

    @staticmethod
    def update_customer(customer, data):

      old_opening = customer.opening_balance

      serializer = CustomerSerializer(
        customer,
        data=data,
        partial=True,
     )

      serializer.is_valid(
        raise_exception=True,
     )

      updated_customer = serializer.save()

      new_opening = updated_customer.opening_balance

      difference = Decimal(new_opening) - Decimal(old_opening)

      if difference != 0:

        updated_customer.current_balance += difference

        updated_customer.save(
            update_fields=[
                "current_balance",
            ]
        )

      return CustomerSerializer(updated_customer).data
    @staticmethod
    def delete_customer(customer):

        customer.delete()

        return {
            "message": "Customer deleted successfully."
        }    

    # ==========================================
    # SUPPLIER
    # ==========================================

    @staticmethod
    def get_suppliers():

        suppliers = Supplier.objects.all()

        serializer = SupplierSerializer(
            suppliers,
            many=True,
        )

        return serializer.data
    
    @staticmethod
    def create_supplier(data):

      serializer = SupplierSerializer(
        data=data,
      )

      serializer.is_valid(
        raise_exception=True,
      )

      serializer.save()

      return serializer.data


    @staticmethod
    def update_supplier(supplier, data):

      serializer = SupplierSerializer(
        supplier,
        data=data,
        partial=True,
      )

      serializer.is_valid(
        raise_exception=True,
      )

      serializer.save()

      return serializer.data


    @staticmethod
    def delete_supplier(supplier):

      supplier.delete()

      return {
        "message": "Supplier deleted successfully."
      }