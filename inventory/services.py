from decimal import Decimal

from django.db.models import (
    Sum,
    F,
    DecimalField,
    ExpressionWrapper,
)

from masters.models import Product

from .models import StockTransaction


class InventoryService:

    # =====================================================
    # RECORD STOCK TRANSACTION
    # =====================================================

    @staticmethod
    def record_transaction(
        product,
        transaction_type,
        quantity,
        reference_number="",
        remarks="",
    ):

        current_stock = product.current_stock

        # -------------------------------
        # Calculate New Stock
        # -------------------------------

        if transaction_type in [
            "OPENING",
            "PURCHASE",
            "ADJUSTMENT_IN",
        ]:

            new_stock = current_stock + quantity

        elif transaction_type in [
            "SALE",
            "ADJUSTMENT_OUT",
            "DAMAGED",
        ]:

            if current_stock < quantity:
                raise ValueError(
                    f"Insufficient stock for "
                    f"{product.product_name}"
                )

            new_stock = current_stock - quantity

        else:
            raise ValueError("Invalid transaction type")

        # -------------------------------
        # Update Product Stock
        # -------------------------------

        product.current_stock = new_stock

        product.stock_value = (
            Decimal(new_stock)
            * product.purchase_price
        )

        product.save()

        # -------------------------------
        # Save Stock Transaction
        # -------------------------------

        StockTransaction.objects.create(

            product=product,

            transaction_type=transaction_type,

            quantity=quantity,

            balance_stock=new_stock,

            reference_number=reference_number,

            remarks=remarks,

        )

        return new_stock

    # =====================================================
    # OPENING STOCK
    # =====================================================

    @staticmethod
    def opening_stock(
        product_id,
        quantity,
        remarks="Opening Stock",
    ):

        product = Product.objects.get(
            id=product_id
        )

        return InventoryService.record_transaction(

            product=product,

            transaction_type="OPENING",

            quantity=quantity,

            remarks=remarks,

        )
    
        # =====================================================
    # PURCHASE STOCK
    # =====================================================

    @staticmethod
    def purchase_stock(
        product_id,
        quantity,
        reference_number="",
        remarks="Purchase",
    ):

        product = Product.objects.get(
            id=product_id
        )

        return InventoryService.record_transaction(

            product=product,

            transaction_type="PURCHASE",

            quantity=quantity,

            reference_number=reference_number,

            remarks=remarks,

        )

    # =====================================================
    # SALE STOCK
    # =====================================================

    @staticmethod
    def sale_stock(
        product_id,
        quantity,
        reference_number="",
        remarks="Sale",
    ):

        product = Product.objects.get(
            id=product_id
        )

        return InventoryService.record_transaction(

            product=product,

            transaction_type="SALE",

            quantity=quantity,

            reference_number=reference_number,

            remarks=remarks,

        )

    # =====================================================
    # PURCHASE INVOICE INTEGRATION
    # =====================================================

    @staticmethod
    def update_purchase_invoice(invoice):

        """
        Call this method immediately after saving
        a PurchaseInvoice.
        """

        for item in invoice.items.all():

            InventoryService.purchase_stock(

                product_id=item.product.id,

                quantity=item.quantity,

                reference_number=invoice.display_invoice_number,

                remarks="Purchase Invoice",

            )

    # =====================================================
    # SALES INVOICE INTEGRATION
    # =====================================================

    @staticmethod
    def update_sales_invoice(invoice):

        """
        Call this method immediately after saving
        a SalesInvoice.
        """

        for item in invoice.items.all():

            InventoryService.sale_stock(

                product_id=item.product.id,

                quantity=item.quantity,

                reference_number=invoice.display_invoice_number,

                remarks="Sales Invoice",

            )

        # =====================================================
    # STOCK ADJUSTMENT IN
    # =====================================================

    @staticmethod
    def adjustment_in(
        product_id,
        quantity,
        remarks="Stock Adjustment In",
    ):

        product = Product.objects.get(
            id=product_id
        )

        return InventoryService.record_transaction(

            product=product,

            transaction_type="ADJUSTMENT_IN",

            quantity=quantity,

            remarks=remarks,

        )

    # =====================================================
    # STOCK ADJUSTMENT OUT
    # =====================================================

    @staticmethod
    def adjustment_out(
        product_id,
        quantity,
        remarks="Stock Adjustment Out",
    ):

        product = Product.objects.get(
            id=product_id
        )

        return InventoryService.record_transaction(

            product=product,

            transaction_type="ADJUSTMENT_OUT",

            quantity=quantity,

            remarks=remarks,

        )

    # =====================================================
    # DAMAGED STOCK
    # =====================================================

    @staticmethod
    def damaged_stock(
        product_id,
        quantity,
        remarks="Damaged Stock",
    ):

        product = Product.objects.get(
            id=product_id
        )

        return InventoryService.record_transaction(

            product=product,

            transaction_type="DAMAGED",

            quantity=quantity,

            remarks=remarks,

        )

    # =====================================================
    # CURRENT STOCK
    # =====================================================

    @staticmethod
    def current_stock(product_id):

        product = Product.objects.get(
            id=product_id
        )

        return {

            "product_id": product.id,

            "product": product.product_name,

            "current_stock": product.current_stock,

            "purchase_price": product.purchase_price,

            "selling_price": product.default_selling_price,

            "stock_value": product.stock_value,

        }

    # =====================================================
    # PRODUCT STOCK SUMMARY
    # =====================================================

    @staticmethod
    def product_stock_summary():

        products = Product.objects.filter(
            is_active=True
        ).order_by("product_name")

        summary = []

        for product in products:

            expected_profit = (
                (
                    product.default_selling_price
                    - product.purchase_price
                )
                * product.current_stock
            )

            summary.append({

                "product_id": product.id,

                "product": product.product_name,

                "stock": product.current_stock,

                "purchase_price": product.purchase_price,

                "selling_price":
                    product.default_selling_price,

                "stock_value":
                    product.stock_value,

                "expected_profit":
                    expected_profit,

            })

        return summary
    
        # =====================================================
    # STOCK REGISTER
    # =====================================================

    @staticmethod
    def stock_register(product_id):

        product = Product.objects.get(
            id=product_id
        )

        transactions = (
            StockTransaction.objects
            .filter(product_id=product_id)
            .order_by("transaction_date", "id")
        )

        register = []

        for transaction in transactions:

            register.append({

                "date":
                    transaction.transaction_date,

                "type":
                    transaction.transaction_type,

                "quantity":
                    transaction.quantity,

                "balance":
                    transaction.balance_stock,

                "reference":
                    transaction.reference_number,

                "remarks":
                    transaction.remarks,

            })

        return {

            "product_id": product.id,

            "product": product.product_name,

            "current_stock":
                product.current_stock,

            "transactions":
                register,

        }

    # =====================================================
    # STOCK MOVEMENT
    # =====================================================

    @staticmethod
    def stock_movement():

        movements = (
            StockTransaction.objects
            .select_related("product")
            .order_by(
                "-transaction_date",
                "-id",
            )
        )

        data = []

        for movement in movements:

            data.append({

                "date":
                    movement.transaction_date,

                "product":
                    movement.product.product_name,

                "type":
                    movement.transaction_type,

                "quantity":
                    movement.quantity,

                "balance":
                    movement.balance_stock,

                "reference":
                    movement.reference_number,

                "remarks":
                    movement.remarks,

            })

        return data

    # =====================================================
    # PRODUCT MOVEMENT
    # =====================================================

    @staticmethod
    def product_movement(product_id):

        product = Product.objects.get(
            id=product_id
        )

        movements = (
            StockTransaction.objects
            .filter(product=product)
            .order_by(
                "-transaction_date",
                "-id",
            )
        )

        result = []

        total_in = 0
        total_out = 0

        for movement in movements:

            if movement.transaction_type in [

                "OPENING",
                "PURCHASE",
                "ADJUSTMENT_IN",

            ]:

                total_in += movement.quantity

            else:

                total_out += movement.quantity

            result.append({

                "date":
                    movement.transaction_date,

                "type":
                    movement.transaction_type,

                "quantity":
                    movement.quantity,

                "balance":
                    movement.balance_stock,

                "reference":
                    movement.reference_number,

            })

        return {

            "product":
                product.product_name,

            "current_stock":
                product.current_stock,

            "stock_in":
                total_in,

            "stock_out":
                total_out,

            "transactions":
                result,

        }
    
        # =====================================================
    # INVENTORY VALUATION
    # =====================================================

    @staticmethod
    def inventory_valuation():

        products = Product.objects.filter(
            is_active=True
        )

        items = []

        total_purchase_value = Decimal("0.00")
        total_selling_value = Decimal("0.00")
        total_expected_profit = Decimal("0.00")

        for product in products:

            purchase_value = (
                Decimal(product.current_stock)
                * product.purchase_price
            )

            selling_value = (
                Decimal(product.current_stock)
                * product.default_selling_price
            )

            expected_profit = (
                selling_value - purchase_value
            )

            items.append({

                "product": product.product_name,

                "stock": product.current_stock,

                "purchase_value": purchase_value,

                "selling_value": selling_value,

                "expected_profit": expected_profit,

            })

            total_purchase_value += purchase_value
            total_selling_value += selling_value
            total_expected_profit += expected_profit

        return {

            "purchase_value": total_purchase_value,

            "selling_value": total_selling_value,

            "expected_profit": total_expected_profit,

            "products": items,

        }


    # =====================================================
    # LOW STOCK REPORT
    # =====================================================

    @staticmethod
    def low_stock_report():

        products = Product.objects.filter(
            is_active=True
        ).order_by("product_name")

        result = []

        for product in products:

            if product.current_stock <= product.minimum_stock:

                result.append({

                    "product_id": product.id,

                    "product": product.product_name,

                    "current_stock":
                        product.current_stock,

                    "minimum_stock":
                        product.minimum_stock,

                })

        return result


    # =====================================================
    # OUT OF STOCK REPORT
    # =====================================================

    @staticmethod
    def out_of_stock_report():

        products = Product.objects.filter(
            is_active=True,
            current_stock=0,
        ).order_by("product_name")

        result = []

        for product in products:

            result.append({

                "product_id": product.id,

                "product": product.product_name,

                "purchase_price":
                    product.purchase_price,

                "selling_price":
                    product.default_selling_price,

            })

        return result


    # =====================================================
    # INVENTORY DASHBOARD
    # =====================================================

    @staticmethod
    def inventory_dashboard():

        products = Product.objects.filter(
            is_active=True
        )

        total_products = products.count()

        total_stock = (
            products.aggregate(
                total=Sum("current_stock")
            )["total"] or 0
        )

        purchase_value = Decimal("0.00")
        selling_value = Decimal("0.00")

        low_stock = 0
        out_of_stock = 0

        for product in products:

            purchase_value += (
                Decimal(product.current_stock)
                * product.purchase_price
            )

            selling_value += (
                Decimal(product.current_stock)
                * product.default_selling_price
            )

            if product.current_stock == 0:

                out_of_stock += 1

            elif product.current_stock <= product.minimum_stock:

                low_stock += 1

        return {

            "total_products": total_products,

            "total_stock": total_stock,

            "purchase_value": purchase_value,

            "selling_value": selling_value,

            "expected_profit":
                selling_value - purchase_value,

            "low_stock_products":
                low_stock,

            "out_of_stock_products":
                out_of_stock,

        }


    # =====================================================
    # INVENTORY SUMMARY
    # =====================================================

    @staticmethod
    def inventory_summary():

        return {

            "dashboard":
                InventoryService.inventory_dashboard(),

            "valuation":
                InventoryService.inventory_valuation(),

            "low_stock":
                InventoryService.low_stock_report(),

            "out_of_stock":
                InventoryService.out_of_stock_report(),

        }