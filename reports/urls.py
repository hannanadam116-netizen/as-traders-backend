from django.urls import path

from .views import (
    SalesReportView,
    PurchaseReportView,
    CustomerWiseSalesView,
    CustomerWiseProfitView,
    ProductWiseSalesView,
    ProductWiseProfitView,
    CustomerLedgerView,
    SupplierLedgerView,
    OutstandingCustomersView,
    OutstandingSuppliersView,
    StockReportView,
    InventoryValuationView,
    LowStockReportView,
    MonthlySalesReportView,
    MonthlyProfitReportView,
    ProfitSummaryView,
    TopCustomersView,
    TopProductsView,
    SalesExcelExportView,
    PurchaseExcelExportView,
    StockExcelExportView,
    SalesAnalyticsView,
    CustomerLedgerExcelExportView,
    SupplierLedgerExcelExportView,
    ProfitReportView,
    ProfitExcelExportView,

    CustomerSalesExcelExportView,
    ProductSalesExcelExportView,
)


urlpatterns = [

    # ==========================================
    # SALES REPORTS
    # ==========================================

    path(
        "sales/",
        SalesReportView.as_view(),
        name="sales-report",
    ),

    path(
        "monthly-sales/",
        MonthlySalesReportView.as_view(),
        name="monthly-sales-report",
    ),

    # ==========================================
    # PURCHASE REPORTS
    # ==========================================

    path(
        "purchases/",
        PurchaseReportView.as_view(),
        name="purchase-report",
    ),

    # ==========================================
    # CUSTOMER REPORTS
    # ==========================================

    path(
        "customer-sales/",
        CustomerWiseSalesView.as_view(),
        name="customer-sales-report",
    ),

    path(
        "customer-profit/",
        CustomerWiseProfitView.as_view(),
        name="customer-profit-report",
    ),

    path(
        "customer-ledger/",
        CustomerLedgerView.as_view(),
        name="customer-ledger",
    ),

    path(
        "customer-outstanding/",
        OutstandingCustomersView.as_view(),
        name="customer-outstanding",
    ),

    path(
        "top-customers/",
        TopCustomersView.as_view(),
        name="top-customers",
    ),

    # ==========================================
    # SUPPLIER REPORTS
    # ==========================================

    path(
        "supplier-ledger/",
        SupplierLedgerView.as_view(),
        name="supplier-ledger",
    ),

    path(
        "supplier-outstanding/",
        OutstandingSuppliersView.as_view(),
        name="supplier-outstanding",
    ),

    # ==========================================
    # PRODUCT REPORTS
    # ==========================================

    path(
        "product-sales/",
        ProductWiseSalesView.as_view(),
        name="product-sales-report",
    ),

    path(
        "product-profit/",
        ProductWiseProfitView.as_view(),
        name="product-profit-report",
    ),

    path(
        "top-products/",
        TopProductsView.as_view(),
        name="top-products",
    ),

    # ==========================================
    # STOCK REPORTS
    # ==========================================

    path(
        "stock/",
        StockReportView.as_view(),
        name="stock-report",
    ),

    path(
        "inventory/",
        InventoryValuationView.as_view(),
        name="inventory-report",
    ),

    path(
        "low-stock/",
        LowStockReportView.as_view(),
        name="low-stock-report",
    ),

    # ==========================================
    # PROFIT REPORTS
    # ==========================================
    path(
      "profit/",
      ProfitReportView.as_view(),
      name="profit-report",
    ),
    path(
        "monthly-profit/",
        MonthlyProfitReportView.as_view(),
        name="monthly-profit-report",
    ),

    path(
        "profit-summary/",
        ProfitSummaryView.as_view(),
        name="profit-summary",
    ),

        path(
        "sales/excel/",
        SalesExcelExportView.as_view(),
        name="sales-excel",
    ),

    path(
        "purchases/excel/",
        PurchaseExcelExportView.as_view(),
        name="purchase-excel",
    ),

    path(
        "stock/excel/",
        StockExcelExportView.as_view(),
        name="stock-excel",
    ),

    path(
        "customer-ledger/excel/",
        CustomerLedgerExcelExportView.as_view(),
        name="customer-ledger-excel",
    ),

    path(
        "supplier-ledger/excel/",
        SupplierLedgerExcelExportView.as_view(),
        name="supplier-ledger-excel",
    ),

    path(
        "profit/excel/",
        ProfitExcelExportView.as_view(),
        name="profit-excel",
    ),

    path(
        "customer-sales/excel/",
        CustomerSalesExcelExportView.as_view(),
        name="customer-sales-excel",
    ),

    path(
        "product-sales/excel/",
        ProductSalesExcelExportView.as_view(),
        name="product-sales-excel",
    ),

    path(
      "sales-analytics/",
      SalesAnalyticsView.as_view(),
    ),
]