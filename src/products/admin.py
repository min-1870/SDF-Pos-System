from django.contrib import admin
from .models import Brand, Barcode, Product, Bundle, ProductBundle


from django.db.models import Subquery, OuterRef, Sum
from transactions.models import TransactionProduct
# Inline for adding/removing products and quantities on the Bundle page
class ProductBundleInline(admin.TabularInline):
    model = ProductBundle
    extra = 1
    fields = ('product', 'quantity')
    verbose_name = "Bundle item"
    verbose_name_plural = "Bundle items"

@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_rate', 'barcode')
    search_fields = ('name',)
    inlines = [ProductBundleInline]

# You probably still want to manage standalone Products
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_rate', 'tax_rate', 'count', 'barcode', 'brand')
    list_filter = ('brand',)
    search_fields = ('name',)
    change_list_template = "admin/product_change_list_with_chart.html"

    def changelist_view(self, request, extra_context=None):
        # get all products
        qs = self.get_queryset(request).order_by('-price')
        labels = [p.name for p in qs]
        data   = [float(p.price) for p in qs]

        extra_context = extra_context or {}
        extra_context['chart_labels'] = labels
        extra_context['chart_data']   = data

        # sold quantity
        
        qs = Product.objects.annotate(
            total=Subquery(
                TransactionProduct.objects.filter(product=OuterRef('pk'))
                .values('product')
                .annotate(sold=Sum('quantity'))
                .values('sold')[:1]
            )
        ).order_by('-total')
        sold_labels = [p.name for p in qs]
        sold_data   = [float(p.total) if p.total is not None else 0 for p in qs]
        extra_context['sold_chart_labels'] = sold_labels
        extra_context['sold_chart_data']   = sold_data

        return super().changelist_view(request, extra_context=extra_context)



