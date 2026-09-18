from rest_framework import serializers

from .models import (
    Category,
    Product,
    Customer,
    Supplier,
    CustomerProductPrice,
)


# ==========================================
# CATEGORY
# ==========================================

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


# ==========================================
# PRODUCT
# ==========================================

class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "category",
            "category_name",
            "purchase_price",
            "default_selling_price",
            "gst_rate",
            "unit",
            "current_stock",
            "is_active",
            "created_at",
            "updated_at",
        ]

        


# ==========================================
# CUSTOMER
# ==========================================

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

        read_only_fields = (
            "current_balance",
        )

    def create(self, validated_data):

        validated_data["current_balance"] = validated_data.get(
            "opening_balance",
            0,
        )

        return super().create(validated_data)


# ==========================================
# SUPPLIER
# ==========================================

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = "__all__"

# ==========================================
# CUSTOMER PRODUCT PRICE
# ==========================================

class CustomerProductPriceSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="customer.name",
        read_only=True,
    )

    product_name = serializers.CharField(
        source="product.product_name",
        read_only=True,
    )

    class Meta:
        model = CustomerProductPrice
        fields = [
            "id",
            "customer",
            "customer_name",
            "product",
            "product_name",
            "selling_price",
        ]