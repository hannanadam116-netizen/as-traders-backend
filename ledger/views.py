from rest_framework.response import Response
from rest_framework.views import APIView

from .services import LedgerService


# =====================================================
# CUSTOMER LEDGER
# =====================================================

class CustomerLedgerView(APIView):

    def get(self, request, customer_id):

        return Response(
            LedgerService.customer_ledger(customer_id)
        )


# =====================================================
# SUPPLIER LEDGER
# =====================================================

class SupplierLedgerView(APIView):

    def get(self, request, supplier_id):

        return Response(
            LedgerService.supplier_ledger(supplier_id)
        )


# =====================================================
# CASH BOOK
# =====================================================

class CashBookView(APIView):

    def get(self, request):

        return Response(
            LedgerService.cash_book()
        )


# =====================================================
# BANK BOOK
# =====================================================

class BankBookView(APIView):

    def get(self, request):

        return Response(
            LedgerService.bank_book()
        )


# =====================================================
# DAY BOOK
# =====================================================

class DayBookView(APIView):

    def get(self, request):

        return Response(
            LedgerService.day_book()
        )


# =====================================================
# CUSTOMER OUTSTANDING
# =====================================================

class CustomerOutstandingView(APIView):

    def get(self, request):

        return Response(
            LedgerService.customer_outstanding()
        )


# =====================================================
# SUPPLIER OUTSTANDING
# =====================================================

class SupplierOutstandingView(APIView):

    def get(self, request):

        return Response(
            LedgerService.supplier_outstanding()
        )


# =====================================================
# TRIAL BALANCE
# =====================================================

class TrialBalanceView(APIView):

    def get(self, request):

        return Response(
            LedgerService.trial_balance()
        )