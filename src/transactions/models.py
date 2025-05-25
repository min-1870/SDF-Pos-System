
import uuid
from django.db import models
from groups.models import Group  # Ensure 'Group' model exists in 'groups' app
from products.models import Product, Bundle  # Ensure 'Product' and 'Bundle' models exist in 'products' app
from decimal import Decimal
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import transaction as db_transaction

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
    transaction_number = models.CharField(max_length=100, blank=True, null=True)
    tax_free = models.BooleanField(default=False)
    till = models.ForeignKey(Till, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    final_gst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    change = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return self.receipt

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_tax_free = None
        if is_new:
            # generate a new transaction number
            self.transaction_number = str(uuid.uuid4())
        else:
            # pull the old record from DB
            old_tax_free = Transaction.objects.values_list('tax_free', flat=True).get(pk=self.pk)

        
        super().save(*args, **kwargs)  # ① actually save the new state

        # ② only recalc if tax_free flipped (or on new)
        if is_new or (old_tax_free != self.tax_free):
            self.recalculate_summary()

    def recalculate_summary(self):
        # 1) Load all items
        items = list(self.transactionproduct_set.all())

        # 2) Re‐apply each item’s promotion/tax logic
        for item in items:
            # final_price is already correct
            if self.tax_free or item.promotion:
                item.final_gst = Decimal('0.00')
            else:
                item.final_gst = (item.final_price * item.product.tax_rate).quantize(Decimal('0.01'))
            item.total = item.final_price + item.final_gst

        # 3) Bulk‐save item changes (no recursion)
        with db_transaction.atomic():
            TransactionProduct.objects.bulk_update(items, ['final_gst', 'total'])

            # 4) Now update the Transaction’s own summary fields
            total_price = sum(i.final_price for i in items)
            total_gst   = sum(i.final_gst   for i in items)
            total       = total_price + total_gst
            payment     = sum(tc.payment / tc.currency.currency_rate for tc in self.transactioncurrency_set.all())
            change      = (total - payment) * -1

            Transaction.objects.filter(pk=self.pk).update(
                final_price=total_price,
                final_gst=total_gst,
                total=total,
                payment=payment,
                change=change,
            )

            
class TransactionCurrency(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    payment = models.DecimalField(max_digits=10, decimal_places=2)

class TransactionProduct(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price= models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    promotion = models.BooleanField(default=False)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    final_gst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        
        if self.promotion:
            self.discount_rate = Decimal('1.00')
            self.price = self.product.price
        else:
            if self.pk is not None:
                previous_promotion = TransactionProduct.objects.filter(pk=self.pk).values_list('promotion', flat=True).first()
                if previous_promotion is not None and previous_promotion:
                    self.discount_rate = Decimal('0.00')
            if self.price is None:
                self.price = self.product.price
            if self.discount_rate is None:
                self.discount_rate = self.product.discount_rate
        
        self.price = round(self.price, 2)
        self.discount_rate = round(self.discount_rate, 2)

        self.final_price = round(
            Decimal(self.price) * (Decimal(1) - Decimal(self.discount_rate)) * Decimal(self.quantity),
            2
        )
        self.final_gst = 0 if self.transaction and self.transaction.tax_free else round((self.final_price * self.product.tax_rate), 2)
        self.total = round(self.final_price+self.final_gst, 2)
        
        super().save(*args, **kwargs)
        # self.transaction.save()

    
    

