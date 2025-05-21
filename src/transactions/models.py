from django.db import models
from groups.models import Group  # Ensure 'Group' model exists in 'groups' app
from products.models import Product, Bundle  # Ensure 'Product' and 'Bundle' models exist in 'products' app

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Till(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=100)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # Use direct reference to 'Group' model
    date_time = models.DateTimeField(auto_now_add=True)
    receipt = models.CharField(max_length=100)
    tax_free = models.BooleanField(default=False)
    till = models.ForeignKey(Till, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class TransactionCurrency(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class TransactionItem(models.Model):
    transaction    = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    item           = GenericForeignKey('content_type', 'object_id')

    custom_price         = models.DecimalField(max_digits=10, decimal_places=2)
    custom_discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    quantity             = models.PositiveIntegerField()

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
