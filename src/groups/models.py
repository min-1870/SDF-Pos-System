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
    
class Place(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, null=True, blank=True)
    group_type = models.ForeignKey(GroupType, on_delete=models.CASCADE)
    tax_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=70)
    default = models.BooleanField()
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    people = models.PositiveIntegerField(default=0)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    

class DefaultGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(default=True)

class DefaultGroup(Group):
    objects = DefaultGroupManager()

    class Meta:
        proxy = True
        verbose_name = 'Group (Default)'
        verbose_name_plural = 'Groups (Default)'

class KrInboundGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type__name='KR Inbound')

class KrInboundGroup(Group):
    objects = KrInboundGroupManager()

    class Meta:
        proxy = True
        verbose_name = 'Group (KR Inbound)'
        verbose_name_plural = 'Groups (KR Inbound)'

class IntInboundGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type__name='INT Inbound')

class IntInboundGroup(Group):
    objects = IntInboundGroupManager()

    class Meta:
        proxy = True
        verbose_name = 'Group (INT Inbound)'
        verbose_name_plural = 'Groups (INT Inbound)'
