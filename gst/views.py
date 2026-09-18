from rest_framework.views import APIView
from rest_framework.response import Response

from .services import GSTService


class GSTSummaryView(APIView):

    def get(self, request):

        return Response(
            GSTService.gst_summary()
        )


class MonthlyGSTSummaryView(APIView):

    def get(self, request):

        return Response(
            GSTService.monthly_gst_summary()
        )


class HSNSummaryView(APIView):

    def get(self, request):

        return Response(
            GSTService.hsn_summary()
        )


class GSTRateSummaryView(APIView):

    def get(self, request):

        return Response(
            GSTService.gst_rate_summary()
        )
    
class GSTR1SummaryView(APIView):

    def get(self, request):

        return Response(
            GSTService.gstr1_summary()
        )


class GSTR3BSummaryView(APIView):

    def get(self, request):

        return Response(
            GSTService.gstr3b_summary()
        )


class InputTaxCreditView(APIView):

    def get(self, request):

        return Response(
            GSTService.input_tax_credit_summary()
        )


class OutputTaxView(APIView):

    def get(self, request):

        return Response(
            GSTService.output_tax_summary()
        )


class GSTDashboardView(APIView):

    def get(self, request):

        return Response(
            GSTService.gst_dashboard()
        )


class GSTReconciliationView(APIView):

    def get(self, request):

        return Response(
            GSTService.gst_reconciliation()
        )


class MonthlyGSTChartView(APIView):

    def get(self, request):

        return Response(
            GSTService.monthly_gst_chart()
        )