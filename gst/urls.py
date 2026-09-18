from django.urls import path

from .views import (
    GSTSummaryView,
    MonthlyGSTSummaryView,
    HSNSummaryView,
    GSTRateSummaryView,
    GSTR1SummaryView,
    GSTR3BSummaryView,
    InputTaxCreditView,
    OutputTaxView,
    GSTDashboardView,
    GSTReconciliationView,
    MonthlyGSTChartView,
)

urlpatterns = [

    path(
        "summary/",
        GSTSummaryView.as_view(),
        name="gst-summary",
    ),

    path(
        "monthly/",
        MonthlyGSTSummaryView.as_view(),
        name="monthly-gst-summary",
    ),

    path(
        "hsn/",
        HSNSummaryView.as_view(),
        name="hsn-summary",
    ),

    path(
        "rates/",
        GSTRateSummaryView.as_view(),
        name="gst-rate-summary",
    ),

    path(
        "gstr1/",
        GSTR1SummaryView.as_view(),
        name="gstr1-summary",
    ),

    path(
        "gstr3b/",
        GSTR3BSummaryView.as_view(),
        name="gstr3b-summary",
    ),

    path(
        "input-tax/",
        InputTaxCreditView.as_view(),
        name="input-tax-credit",
    ),

    path(
        "output-tax/",
        OutputTaxView.as_view(),
        name="output-tax",
    ),

    path(
        "dashboard/",
        GSTDashboardView.as_view(),
        name="gst-dashboard",
    ),

    path(
        "reconciliation/",
        GSTReconciliationView.as_view(),
        name="gst-reconciliation",
    ),

    path(
        "chart/",
        MonthlyGSTChartView.as_view(),
        name="monthly-gst-chart",
    ),
]