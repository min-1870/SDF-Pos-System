from django.db import models
from groups.models import Group  # Ensure 'Group' model exists in 'groups' app
from products.models import Product, Bundle  # Ensure 'Product' and 'Bundle' models exist in 'products' app

class Till(models.Model):
    name = models.CharField(max_length=100)

class Currency(models.Model):
    name = models.CharField(max_length=100)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class Transaction(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # Use direct reference to 'Group' model
    date_time = models.DateTimeField()
    receipt = models.CharField(max_length=100)
    tax_free = models.BooleanField(default=False)
    till = models.ForeignKey(Till, on_delete=models.CASCADE)

class TransactionCurrency(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class TransactionProduct(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Use direct reference to 'Product' model
    custom_price = models.DecimalField(max_digits=10, decimal_places=2)
    custom_discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()

class TransactionBundle(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)  # Use direct reference to 'Bundle' model
    custom_price = models.DecimalField(max_digits=10, decimal_places=2)
    custom_discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
