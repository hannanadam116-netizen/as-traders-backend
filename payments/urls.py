from django.urls import path

from .views import (
    CustomerPaymentListCreateView,
    CustomerPaymentDetailView,
    SupplierPaymentListCreateView,
    SupplierPaymentDetailView,
)

urlpatterns = [

    # Customer Payments

    path(
        "customer-payments/",
        CustomerPaymentListCreateView.as_view(),
        name="customer-payment-list-create",
    ),

    path(
        "customer-payments/<int:pk>/",
        CustomerPaymentDetailView.as_view(),
        name="customer-payment-detail",
    ),

    # Supplier Payments

    path(
        "supplier-payments/",
        SupplierPaymentListCreateView.as_view(),
        name="supplier-payment-list-create",
    ),

    path(
        "supplier-payments/<int:pk>/",
        SupplierPaymentDetailView.as_view(),
        name="supplier-payment-detail",
    ),
]