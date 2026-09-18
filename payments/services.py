from decimal import Decimal

from django.db import transaction
from django.db.models import Max

from masters.models import Customer, Supplier
from django.db.models import F
from .models import (
    CustomerPayment,
    SupplierPayment,
)


# =====================================================
# CUSTOMER PAYMENT SERVICE
# =====================================================

class CustomerPaymentService:

    @staticmethod
    def _get_next_receipt_number():

        last = CustomerPayment.objects.aggregate(
            Max("receipt_number")
        )["receipt_number__max"]

        if last is None:
            return 1

        return last + 1

    @staticmethod
    @transaction.atomic
    def create_payment(data):

        customer = data["customer"]

        amount = Decimal(data["amount"])

        if amount <= 0:
            raise ValueError(
                "Payment amount must be greater than zero."
            )

        payment = CustomerPayment.objects.create(
            receipt_number=CustomerPaymentService._get_next_receipt_number(),
            payment_date=data["payment_date"],
            customer=customer,
            amount=amount,
            payment_mode=data["payment_mode"],
            remarks=data.get("remarks", ""),
        )

        Customer.objects.filter(
         pk=customer.pk,
        ).update(
         current_balance=F("current_balance") - amount
        )

        return payment
    @staticmethod
    def delete_payment(payment):

      customer = payment.customer

      customer.current_balance += payment.amount
      customer.save(
        update_fields=["current_balance"]
    )


      payment.delete()

# =====================================================
# SUPPLIER PAYMENT SERVICE
# =====================================================

class SupplierPaymentService:

    @staticmethod
    def _get_next_receipt_number():

        last = SupplierPayment.objects.aggregate(
            Max("receipt_number")
        )["receipt_number__max"]

        if last is None:
            return 1

        return last + 1

    @staticmethod
    @transaction.atomic
    def create_payment(data):

        supplier = data["supplier"]

        amount = Decimal(data["amount"])

        if amount <= 0:
            raise ValueError(
                "Payment amount must be greater than zero."
            )

        payment = SupplierPayment.objects.create(
            receipt_number=SupplierPaymentService._get_next_receipt_number(),
            payment_date=data["payment_date"],
            supplier=supplier,
            amount=amount,
            payment_mode=data["payment_mode"],
            remarks=data.get("remarks", ""),
        )

        supplier.current_balance -= amount

        supplier.save(
            update_fields=[
                "current_balance",
            ]
        )

        return payment
    
    @staticmethod
    def delete_payment(payment):

      supplier = payment.supplier

      supplier.current_balance += payment.amount
      supplier.save(
        update_fields=["current_balance"]
    )
  
      payment.delete()