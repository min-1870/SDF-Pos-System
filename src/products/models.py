from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Barcode(models.Model):
    barcode = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.barcode

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.PositiveIntegerField()
    barcode = models.ForeignKey(Barcode, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class Bundle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    barcode = models.ForeignKey(Barcode, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bundle {self.id}"

class ProductBundle(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('product', 'bundle')

    def __str__(self):
        return f"{self.product.name} x{self.quantity} in Bundle {self.bundle.id}"
