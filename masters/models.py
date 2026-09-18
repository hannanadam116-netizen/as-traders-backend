from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    

    product_name = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    gst_rate = models.DecimalField(
      max_digits=5,
      decimal_places=2,
      default=0,
    )

    default_selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    unit = models.CharField(
      max_length=20,
      default="Bag",
    )

    current_stock = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product_name"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Customer(models.Model):
    name = models.CharField(max_length=200)

    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    gst_number = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(blank=True)

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pin_code = models.CharField(
        max_length=10,
        blank=True
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    current_balance = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=0
    )

    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
   

class Supplier(models.Model):
    name = models.CharField(max_length=200)

    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    gst_number = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(blank=True)

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pin_code = models.CharField(
        max_length=10,
        blank=True
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    current_balance = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=0
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class CustomerProductPrice(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="product_prices"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="customer_prices"
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        unique_together = ("customer", "product")
        ordering = ["customer__name", "product__product_name"]

    def __str__(self):
        return f"{self.customer.name} - {self.product.product_name}"