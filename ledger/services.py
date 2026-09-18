from decimal import Decimal

from django.db.models import Sum

from masters.models import (
    Customer,
    Supplier,
)

from transactions.models import (
    SalesInvoice,
)

from purchases.models import (
    PurchaseInvoice,
)

from payments.models import (
    CustomerPayment,
    SupplierPayment,
)
from django.shortcuts import get_object_or_404

class LedgerService:

    # =====================================================
    # CUSTOMER LEDGER
    # =====================================================

    @staticmethod
    def customer_ledger(customer_id):

        customer = get_object_or_404(
         Customer,
         id=customer_id,
        )
        ledger = []

        balance = customer.opening_balance or Decimal("0.00")

        # Opening Balance

        ledger.append({

            "date": None,

            "particular": "Opening Balance",

            "debit": Decimal("0.00"),

            "credit": Decimal("0.00"),

            "balance": balance,

        })

        # Sales Invoices

        invoices = (
            SalesInvoice.objects
            .filter(customer_id=customer_id)
            .order_by("invoice_date", "invoice_number")
        )

        for invoice in invoices:

            balance += invoice.grand_total

            ledger.append({

                "date": invoice.invoice_date,

                "particular":
                    f"Sales Invoice {invoice.display_invoice_number}",

                "debit": invoice.grand_total,

                "credit": Decimal("0.00"),

                "balance": balance,

            })

        # Customer Payments

        payments = (
            CustomerPayment.objects
            .filter(customer_id=customer_id)
            .order_by("payment_date", "receipt_number")
        )

        for payment in payments:

            balance -= payment.amount

            ledger.append({

                "date": payment.payment_date,

                "particular":
                    f"Receipt {payment.display_receipt_number}",

                "debit": Decimal("0.00"),

                "credit": payment.amount,

                "balance": balance,

            })

        return {

            "customer": customer.name,

            "opening_balance":
                customer.opening_balance,

            "closing_balance":
                balance,

            "ledger": ledger,

        }
    
        # =====================================================
    # SUPPLIER LEDGER
    # =====================================================

    @staticmethod
    def supplier_ledger(supplier_id):

        supplier = get_object_or_404(
          Supplier,
          id=supplier_id,
        )

        ledger = []

        balance = supplier.opening_balance or Decimal("0.00")

        # Opening Balance

        ledger.append({

            "date": None,

            "particular": "Opening Balance",

            "debit": Decimal("0.00"),

            "credit": Decimal("0.00"),

            "balance": balance,

        })

        # Purchase Invoices

        invoices = (
            PurchaseInvoice.objects
            .filter(supplier_id=supplier_id)
            .order_by("invoice_date", "invoice_number")
        )

        for invoice in invoices:

            balance += invoice.grand_total

            ledger.append({

                "date": invoice.invoice_date,

                "particular":
                    f"Purchase Invoice {invoice.display_invoice_number}",

                "debit": invoice.grand_total,

                "credit": Decimal("0.00"),

                "balance": balance,

            })

        # Supplier Payments

        payments = (
            SupplierPayment.objects
            .filter(supplier_id=supplier_id)
            .order_by("payment_date", "receipt_number")
        )

        for payment in payments:

            balance -= payment.amount

            ledger.append({

                "date": payment.payment_date,

                "particular":
                    f"Payment {payment.display_receipt_number}",

                "debit": Decimal("0.00"),

                "credit": payment.amount,

                "balance": balance,

            })

        return {

            "supplier": supplier.name,

            "opening_balance":
                supplier.opening_balance,

            "closing_balance":
                balance,

            "ledger": ledger,

        }
    
        # =====================================================
    # CASH BOOK
    # =====================================================

    @staticmethod
    def cash_book():

        transactions = []

        # Customer Cash Receipts
        receipts = CustomerPayment.objects.filter(
            payment_mode="Cash"
        ).order_by("payment_date")

        for receipt in receipts:

            transactions.append({

                "date": receipt.payment_date,

                "particular":
                    f"Receipt - {receipt.customer.name}",

                "receipt": receipt.amount,

                "payment": Decimal("0.00"),

            })

        # Supplier Cash Payments
        payments = SupplierPayment.objects.filter(
            payment_mode="Cash"
        ).order_by("payment_date")

        for payment in payments:

            transactions.append({

                "date": payment.payment_date,

                "particular":
                    f"Payment - {payment.supplier.name}",

                "receipt": Decimal("0.00"),

                "payment": payment.amount,

            })

        transactions.sort(key=lambda x: x["date"])

        balance = Decimal("0.00")

        for row in transactions:

            balance += row["receipt"]
            balance -= row["payment"]

            row["balance"] = balance

        return {

            "closing_balance": balance,

            "transactions": transactions,

        }


    # =====================================================
    # BANK BOOK
    # =====================================================

    @staticmethod
    def bank_book():

        transactions = []

        # Customer Bank Receipts
        receipts = CustomerPayment.objects.filter(
            payment_mode="Bank"
        ).order_by("payment_date")

        for receipt in receipts:

            transactions.append({

                "date": receipt.payment_date,

                "particular":
                    f"Receipt - {receipt.customer.name}",

                "receipt": receipt.amount,

                "payment": Decimal("0.00"),

            })

        # Supplier Bank Payments
        payments = SupplierPayment.objects.filter(
            payment_mode="Bank"
        ).order_by("payment_date")

        for payment in payments:

            transactions.append({

                "date": payment.payment_date,

                "particular":
                    f"Payment - {payment.supplier.name}",

                "receipt": Decimal("0.00"),

                "payment": payment.amount,

            })

        transactions.sort(key=lambda x: x["date"])

        balance = Decimal("0.00")

        for row in transactions:

            balance += row["receipt"]
            balance -= row["payment"]

            row["balance"] = balance

        return {

            "closing_balance": balance,

            "transactions": transactions,

        }
    
        # =====================================================
    # DAY BOOK
    # =====================================================

    @staticmethod
    def day_book():

        entries = []

        # ---------------------------------------------
        # SALES
        # ---------------------------------------------

        sales = (
            SalesInvoice.objects
            .select_related("customer")
            .order_by("invoice_date", "invoice_number")
        )

        for sale in sales:

            entries.append({

                "date": sale.invoice_date,

                "type": "Sales",

                "voucher":
                    sale.display_invoice_number,

                "party":
                    sale.customer.name,

                "debit":
                    sale.grand_total,

                "credit":
                    Decimal("0.00"),

            })

        # ---------------------------------------------
        # PURCHASES
        # ---------------------------------------------

        purchases = (
            PurchaseInvoice.objects
            .select_related("supplier")
            .order_by("invoice_date", "invoice_number")
        )

        for purchase in purchases:

            entries.append({

                "date": purchase.invoice_date,

                "type": "Purchase",

                "voucher":
                    purchase.display_invoice_number,

                "party":
                    purchase.supplier.name,

                "debit":
                    Decimal("0.00"),

                "credit":
                    purchase.grand_total,

            })

        # ---------------------------------------------
        # CUSTOMER RECEIPTS
        # ---------------------------------------------

        receipts = (
            CustomerPayment.objects
            .select_related("customer")
            .order_by("payment_date", "receipt_number")
        )

        for receipt in receipts:

            entries.append({

                "date": receipt.payment_date,

                "type": "Receipt",

                "voucher":
                    receipt.display_receipt_number,

                "party":
                    receipt.customer.name,

                "debit":
                    Decimal("0.00"),

                "credit":
                    receipt.amount,

            })

        # ---------------------------------------------
        # SUPPLIER PAYMENTS
        # ---------------------------------------------

        payments = (
            SupplierPayment.objects
            .select_related("supplier")
            .order_by("payment_date", "receipt_number")
        )

        for payment in payments:

            entries.append({

                "date": payment.payment_date,

                "type": "Payment",

                "voucher":
                    payment.display_receipt_number,

                "party":
                    payment.supplier.name,

                "debit":
                    payment.amount,

                "credit":
                    Decimal("0.00"),

            })

        entries.sort(
            key=lambda row: (
                row["date"],
            )
        )

        return entries
    
        # =====================================================
    # CUSTOMER OUTSTANDING
    # =====================================================

    @staticmethod
    def customer_outstanding():

        customers = Customer.objects.filter(
            is_active=True
        ).order_by("name")

        result = []

        total = Decimal("0.00")

        for customer in customers:

            balance = customer.current_balance or Decimal("0.00")

            result.append({

                "customer_id": customer.id,

                "customer": customer.name,

                "mobile": customer.mobile,

                "balance": balance,

            })

            total += balance

        return {

            "total_outstanding": total,

            "customers": result,

        }


    # =====================================================
    # SUPPLIER OUTSTANDING
    # =====================================================

    @staticmethod
    def supplier_outstanding():

        suppliers = Supplier.objects.filter(
            is_active=True
        ).order_by("name")

        result = []

        total = Decimal("0.00")

        for supplier in suppliers:

            balance = supplier.current_balance or Decimal("0.00")

            result.append({

                "supplier_id": supplier.id,

                "supplier": supplier.name,

                "mobile": supplier.mobile,

                "balance": balance,

            })

            total += balance

        return {

            "total_outstanding": total,

            "suppliers": result,

        }


    # =====================================================
    # TRIAL BALANCE
    # =====================================================

    @staticmethod
    def trial_balance():

        customer_total = (
            Customer.objects.aggregate(
                total=Sum("current_balance")
            )["total"]
            or Decimal("0.00")
        )

        supplier_total = (
            Supplier.objects.aggregate(
                total=Sum("current_balance")
            )["total"]
            or Decimal("0.00")
        )

        cash = LedgerService.cash_book()

        bank = LedgerService.bank_book()

        return {

            "customers": customer_total,

            "suppliers": supplier_total,

            "cash_balance":
                cash["closing_balance"],

            "bank_balance":
                bank["closing_balance"],

            "total_assets":
                customer_total
                + cash["closing_balance"]
                + bank["closing_balance"],

            "total_liabilities":
                supplier_total,

        }