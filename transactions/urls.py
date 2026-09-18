from django.urls import path

from .views import (
    SalesInvoiceListCreateView,
    SalesInvoiceDetailView,
    SalesInvoicePDFView,
    TodaySalesListView
)

urlpatterns = [
    path(
        "sales/",
        SalesInvoiceListCreateView.as_view(),
        name="sales-list-create",
    ),

    path(
        "sales/<int:pk>/",
        SalesInvoiceDetailView.as_view(),
        name="sales-detail",
    ),
    path(
      "sales/today/",
      TodaySalesListView.as_view(),
    ),

    path(
      "sales/<int:pk>/pdf/",
      SalesInvoicePDFView.as_view(),
      name="sales-invoice-pdf",
    ),
]