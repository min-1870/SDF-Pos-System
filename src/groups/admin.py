from django.contrib import admin
from .models import Guide, Group, DefaultGroup, IntInboundGroup, KrInboundGroup
from django.contrib import admin
from django.template.response import TemplateResponse
from products.models import Product

from django.db.models import Subquery, OuterRef, Sum
from transactions.models import TransactionProduct, Transaction

# admin.site.index_template = "admin/index.html"

def custom_index(request, extra_context=None):
        qs = Product.objects.order_by('-price')
        labels = [p.name for p in qs]
        data   = [float(p.price) for p in qs]

        site   = admin.site           # shortcut
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

        
        # #default group
        
        group_totals = Group.objects.filter(
             default=True
        ).annotate(
            total=Subquery(
                Transaction.objects.filter(group=OuterRef('pk'))
                .values('group')
                .annotate(total_sum=Sum('total'))
                .values('total_sum')[:1]
            )
        )
        labels = [group.name for group in group_totals]
        data   = [round(float(group.total),2) if group.total is not None else 0 for group in group_totals]
        extra_context = extra_context or {}
        extra_context['default_chart_labels'] = labels
        extra_context['default_chart_data']   = data
        extra_context['total'] = sum(extra_context['default_chart_data'])

        # kr inbound group
        group_totals = Group.objects.filter(
             group_type__name='KR Inbound'
        ).annotate(
            total=Subquery(
                Transaction.objects.filter(group=OuterRef('pk'))
                .values('group')
                .annotate(total_sum=Sum('total'))
                .values('total_sum')[:1]
            )
        )
        labels = [group.name for group in group_totals]
        data   = [round(float(group.total),2) if group.total is not None else 0 for group in group_totals]
        extra_context = extra_context or {}
        extra_context['kr_chart_labels'] = labels
        extra_context['kr_chart_data']   = data
        extra_context['total'] += sum(extra_context['kr_chart_data'])

        # int inbound group
        group_totals = Group.objects.filter(
             group_type__name='INT Inbound'
        ).annotate(
            total=Subquery(
                Transaction.objects.filter(group=OuterRef('pk'))
                .values('group')
                .annotate(total_sum=Sum('total'))
                .values('total_sum')[:1]
            )
        )
        labels = [group.name for group in group_totals]
        data   = [round(float(group.total),2) if group.total is not None else 0 for group in group_totals]
        extra_context = extra_context or {}
        extra_context['int_chart_labels'] = labels
        extra_context['int_chart_data']   = data
        extra_context['total'] += sum(extra_context['int_chart_data'])
        extra_context['total'] = round(float(extra_context['total']),2)

        # Merge contexts and render:
        context = {
            **site.each_context(request),          # logo, user-menu, etc.
            "title": site.index_title or _("Site administration"),
            "app_list": site.get_app_list(request),  # <-- the missing piece
            **extra_context,
        }
        return TemplateResponse(request, "admin/index.html", context)


admin.site.index = custom_index

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'tc_rate', 'company', 'contact')
    search_fields = ('name',)

@admin.register(DefaultGroup)
class GroupDefaultAdmin(admin.ModelAdmin):

    list_display = ('name', 'group_type', 'tax_threshold', 'default')
    change_list_template = "admin/group_change_list.html"
    def changelist_view(self, request, extra_context=None):
        group_totals = Group.objects.filter(
             default=True
        ).annotate(
            total=Subquery(
                Transaction.objects.filter(group=OuterRef('pk'))
                .values('group')
                .annotate(total_sum=Sum('total'))
                .values('total_sum')[:1]
            )
        )
        labels = [group.name for group in group_totals]
        data   = [round(float(group.total),2) if group.total is not None else 0 for group in group_totals]
        extra_context = extra_context or {}
        extra_context['chart_labels'] = labels
        extra_context['chart_data']   = data

        return super().changelist_view(request, extra_context=extra_context)

@admin.register(KrInboundGroup)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'group_type', 'date', 'time', 'place', 'people', 'guide', 'company', 'tax_threshold')
    list_filter = ('date',)
    change_list_template = "admin/group_change_list.html"

    def company(self, obj):
        return obj.guide.company.name if obj.guide and obj.guide.company else None
    company.short_description = 'Company'
    

    def changelist_view(self, request, extra_context=None):
        group_totals = Group.objects.filter(
             group_type__name='KR Inbound'
        ).annotate(
            total=Subquery(
                Transaction.objects.filter(group=OuterRef('pk'))
                .values('group')
                .annotate(total_sum=Sum('total'))
                .values('total_sum')[:1]
            )
        )
        labels = [group.name for group in group_totals]
        data   = [round(float(group.total),2) if group.total is not None else 0 for group in group_totals]
        extra_context = extra_context or {}
        extra_context['chart_labels'] = labels
        extra_context['chart_data']   = data

        return super().changelist_view(request, extra_context=extra_context)

    
@admin.register(IntInboundGroup)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'group_type', 'date', 'time', 'place', 'people', 'guide', 'company', 'tax_threshold')
    list_filter = ('date',)
    change_list_template = "admin/group_change_list.html"

    def company(self, obj):
        return obj.guide.company.name if obj.guide and obj.guide.company else None
    company.short_description = 'Company'
    
    def changelist_view(self, request, extra_context=None):
        group_totals = Group.objects.filter(
             group_type__name='INT Inbound'
        ).annotate(
            total=Subquery(
                Transaction.objects.filter(group=OuterRef('pk'))
                .values('group')
                .annotate(total_sum=Sum('total'))
                .values('total_sum')[:1]
            )
        )
        labels = [group.name for group in group_totals]
        data   = [round(float(group.total),2) if group.total is not None else 0 for group in group_totals]
        extra_context = extra_context or {}
        extra_context['chart_labels'] = labels
        extra_context['chart_data']   = data

        return super().changelist_view(request, extra_context=extra_context)

