from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Guide(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    tc_rate = models.DecimalField(max_digits=5, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class GroupType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    group_type = models.ForeignKey(GroupType, on_delete=models.CASCADE)
    tax_threshold = models.DecimalField(max_digits=10, decimal_places=2)
    default = models.BooleanField()
    date = models.DateField()

    def __str__(self):
        return self.name
