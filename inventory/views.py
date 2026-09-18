from rest_framework.response import Response
from rest_framework.views import APIView

from .services import InventoryService


# =====================================================
# INVENTORY SUMMARY
# =====================================================

class InventorySummaryView(APIView):

    def get(self, request):

        return Response(
            InventoryService.inventory_summary()
        )


# =====================================================
# INVENTORY DASHBOARD
# =====================================================

class InventoryDashboardView(APIView):

    def get(self, request):

        return Response(
            InventoryService.inventory_dashboard()
        )


# =====================================================
# INVENTORY VALUATION
# =====================================================

class InventoryValuationView(APIView):

    def get(self, request):

        return Response(
            InventoryService.inventory_valuation()
        )


# =====================================================
# PRODUCT STOCK SUMMARY
# =====================================================

class ProductStockSummaryView(APIView):

    def get(self, request):

        return Response(
            InventoryService.product_stock_summary()
        )


# =====================================================
# CURRENT STOCK
# =====================================================

class CurrentStockView(APIView):

    def get(self, request, product_id):

        return Response(
            InventoryService.current_stock(product_id)
        )


# =====================================================
# STOCK REGISTER
# =====================================================

class StockRegisterView(APIView):

    def get(self, request, product_id):

        return Response(
            InventoryService.stock_register(product_id)
        )


# =====================================================
# PRODUCT MOVEMENT
# =====================================================

class ProductMovementView(APIView):

    def get(self, request, product_id):

        return Response(
            InventoryService.product_movement(product_id)
        )


# =====================================================
# STOCK MOVEMENT
# =====================================================

class StockMovementView(APIView):

    def get(self, request):

        return Response(
            InventoryService.stock_movement()
        )


# =====================================================
# LOW STOCK
# =====================================================

class LowStockView(APIView):

    def get(self, request):

        return Response(
            InventoryService.low_stock_report()
        )


# =====================================================
# OUT OF STOCK
# =====================================================

class OutOfStockView(APIView):

    def get(self, request):

        return Response(
            InventoryService.out_of_stock_report()
        )