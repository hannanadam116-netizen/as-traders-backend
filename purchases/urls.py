from django.urls import path

from .views import (
    PurchaseInvoiceListCreateView,
    PurchaseInvoiceDetailView,
    PurchaseInvoicePDFView,
    TodayPurchaseListView
)

urlpatterns = [

    path(
        "purchases/",
        PurchaseInvoiceListCreateView.as_view(),
        name="purchase-list-create",
    ),
    path(
      "purchases/today/",
      TodayPurchaseListView.as_view(),
    ),
    path(
        "purchases/<int:pk>/",
        PurchaseInvoiceDetailView.as_view(),
        name="purchase-detail",
    ),

    path(
      "purchases/<int:pk>/pdf/",
      PurchaseInvoicePDFView.as_view(),
      name="purchase-invoice-pdf",
    ),
   
]