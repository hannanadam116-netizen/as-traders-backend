from django.urls import path

from .views import (
    CategoryListCreateView,
    ProductListCreateView,
    ProductDetailView,
    SupplierListCreateView,
     SupplierDetailView,
    CustomerListCreateView,
    CustomerDetailView,
    OutstandingCustomerListView,
    OutstandingSupplierListView,
    CustomerProductPriceListCreateView,
    CustomerProductPriceDetailView,
)

urlpatterns = [

    # ==========================================
    # CATEGORY
    # ==========================================

    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="category-list-create",
    ),

    # ==========================================
    # PRODUCT
    # ==========================================

    path(
        "products/",
        ProductListCreateView.as_view(),
        name="product-list-create",
    ),

    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),

    # ==========================================
    # CUSTOMER
    # ==========================================
    path(
      "customers/",
       CustomerListCreateView.as_view(),
       name="customer-list-create",
    ),
    path(
          "customers/outstanding/",
          OutstandingCustomerListView.as_view(),
        ),
    

    path(
        "customers/<int:pk>/",
        CustomerDetailView.as_view(),
        name="customer-detail",
    ),

    path(
      "customer-product-prices/",
      CustomerProductPriceListCreateView.as_view(),
      name="customer-product-price-list",
    ),

    path(
      "customer-product-prices/<int:pk>/",
      CustomerProductPriceDetailView.as_view(),
      name="customer-product-price-detail",
    ),

    # ==========================================
    # SUPPLIER
    # ==========================================

    path(
      "suppliers/",
      SupplierListCreateView.as_view(),
      name="supplier-list-create",
    ),
    path(
      "suppliers/outstanding/",
      OutstandingSupplierListView.as_view(),
    ),

    path(
      "suppliers/<int:pk>/",
      SupplierDetailView.as_view(),
      name="supplier-detail",
    ),
]