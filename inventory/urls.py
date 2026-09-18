from django.urls import path

from .views import (
    InventorySummaryView,
    InventoryDashboardView,
    InventoryValuationView,
    ProductStockSummaryView,
    CurrentStockView,
    StockRegisterView,
    ProductMovementView,
    StockMovementView,
    LowStockView,
    OutOfStockView,
)

urlpatterns = [

    # ==========================================
    # INVENTORY SUMMARY
    # ==========================================

    path(
        "summary/",
        InventorySummaryView.as_view(),
        name="inventory-summary",
    ),

    path(
        "dashboard/",
        InventoryDashboardView.as_view(),
        name="inventory-dashboard",
    ),

    path(
        "valuation/",
        InventoryValuationView.as_view(),
        name="inventory-valuation",
    ),

    # ==========================================
    # PRODUCT STOCK
    # ==========================================

    path(
        "products/",
        ProductStockSummaryView.as_view(),
        name="product-stock-summary",
    ),

    path(
        "current-stock/<int:product_id>/",
        CurrentStockView.as_view(),
        name="current-stock",
    ),

    # ==========================================
    # STOCK REGISTER
    # ==========================================

    path(
        "stock-register/<int:product_id>/",
        StockRegisterView.as_view(),
        name="stock-register",
    ),

    path(
        "product-movement/<int:product_id>/",
        ProductMovementView.as_view(),
        name="product-movement",
    ),

    path(
        "stock-movement/",
        StockMovementView.as_view(),
        name="stock-movement",
    ),

    # ==========================================
    # STOCK REPORTS
    # ==========================================

    path(
        "low-stock/",
        LowStockView.as_view(),
        name="low-stock",
    ),

    path(
        "out-of-stock/",
        OutOfStockView.as_view(),
        name="out-of-stock",
    ),
]