from django.urls import path

from .views import (
    CustomerLedgerView,
    SupplierLedgerView,
    CashBookView,
    BankBookView,
    DayBookView,
    CustomerOutstandingView,
    SupplierOutstandingView,
    TrialBalanceView,
)

urlpatterns = [

    # ==========================================
    # CUSTOMER LEDGER
    # ==========================================

    path(
        "customer/<int:customer_id>/",
        CustomerLedgerView.as_view(),
        name="customer-ledger",
    ),

    # ==========================================
    # SUPPLIER LEDGER
    # ==========================================

    path(
        "supplier/<int:supplier_id>/",
        SupplierLedgerView.as_view(),
        name="supplier-ledger",
    ),

    # ==========================================
    # CASH BOOK
    # ==========================================

    path(
        "cash-book/",
        CashBookView.as_view(),
        name="cash-book",
    ),

    # ==========================================
    # BANK BOOK
    # ==========================================

    path(
        "bank-book/",
        BankBookView.as_view(),
        name="bank-book",
    ),

    # ==========================================
    # DAY BOOK
    # ==========================================

    path(
        "day-book/",
        DayBookView.as_view(),
        name="day-book",
    ),

    # ==========================================
    # OUTSTANDING
    # ==========================================

    path(
        "customer-outstanding/",
        CustomerOutstandingView.as_view(),
        name="customer-outstanding",
    ),

    path(
        "supplier-outstanding/",
        SupplierOutstandingView.as_view(),
        name="supplier-outstanding",
    ),

    # ==========================================
    # TRIAL BALANCE
    # ==========================================

    path(
        "trial-balance/",
        TrialBalanceView.as_view(),
        name="trial-balance",
    ),
]