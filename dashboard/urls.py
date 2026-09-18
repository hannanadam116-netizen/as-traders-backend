from django.urls import path

from .views import(DashboardSummaryView,
                   TodaySalesView,
    TodayPurchasesView,
    CustomerOutstandingView,
    SupplierOutstandingView,)

urlpatterns = [

    path(
        "dashboard/summary/",
        DashboardSummaryView.as_view(),
        name="dashboard-summary",
    ),
    path(
        "today-sales/",
        TodaySalesView.as_view(),
    ),

    path(
        "today-purchases/",
        TodayPurchasesView.as_view(),
    ),

    path(
        "receivables/",
        CustomerOutstandingView.as_view(),
    ),

    path(
        "payables/",
        SupplierOutstandingView.as_view(),
    ),


]