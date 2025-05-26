from django.utils.html import format_html
from django.db import models
from django.db.models import Subquery, OuterRef, Sum

from django.contrib import admin
from .models import Transaction, TransactionProduct, TransactionCurrency, Currency, Till
from .forms  import TransactionProductInlineForm, TransactionCurrencyInlineForm
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from groups.models import Group
# (If you also want bundles inline, you can make a similar form and inline for TransactionBundle.)

@admin.register(Currency)
class GroupDefaultAdmin(admin.ModelAdmin):

    list_display = ('name', 'currency_rate', 'date')
    

class TransactionCurrencyInline(admin.TabularInline):
    model = TransactionCurrency
    form = TransactionCurrencyInlineForm
    extra = 1

class TransactionProductInline(admin.TabularInline):
    model = TransactionProduct          
    form  = TransactionProductInlineForm  
    extra = 1

@admin.register(Till)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'cashUp')
    change_list_template = "admin/transaction_change_list.html"

    def changelist_view(self, request, extra_context=None):
        till_totals = Till.objects.annotate(
            total=Subquery(
                Transaction.objects.filter(till=OuterRef('pk'))
                .values('till')
                .annotate(total_sum=Sum('total'))
                .values('total_sum')[:1]
            )
        )
        # Example: print or use group_totals as needed
        for till in till_totals:
            print(f"Till: {till.name}, Total: {till.total}")
        
        labels = [till.name for till in till_totals]
        data   = [round(float(till.total),2) for till in till_totals]
        extra_context = {}
        extra_context['chart_labels'] = labels
        extra_context['chart_data']   = data
        extra_context['total'] = sum(extra_context['chart_data'])

        return super().changelist_view(request, extra_context=extra_context)

    def cashUp(self, obj):
        data = {}
        till_instance = Till.objects.get(name=obj.name)
        currencies = Currency.objects.all()
        for currency in currencies:
            data[currency.name] = TransactionCurrency.objects.filter(
                transaction__till=till_instance, currency=currency
            ).aggregate(
                total_payment=models.Sum('payment')
            )['total_payment'] or 0.00

        col_width = 120  # px, adjust as needed
        html = f'<table style="border-collapse: collapse; width: 100%; background: none;"><tr>'
        for currency_name in data.keys():
            html += (
            f"<th style='padding:4px; border:1px solid #ddd; width:{col_width}px; min-width:{col_width}px; max-width:{col_width}px; text-align:center;'>"
            f"<b>{currency_name}</b></th>"
            )
        html += "</tr><tr>"
        for total in data.values():
            html += (
            f"<td style='padding:4px; border:1px solid #eee; text-align:center; width:{col_width}px; min-width:{col_width}px; max-width:{col_width}px;'>"
            f"{total:.2f}</td>"
            )
        html += "</tr></table>"

        return format_html(html)
    cashUp.short_description = "Summary"

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('total', 'group', 'till', 'date_time', 'tax_free','final_price', 'final_gst', 'payment', 'change', 'receipt', 'transaction_number',)
    readonly_fields = (
        'transaction_number', 'receipt',
        'product_snapshot','payment_snapshot','spacer',
        'final_price', 'final_gst', 'total',
        'payment', 'change',
    )
    list_filter = ('group','till','date_time', 'tax_free', 'transaction_number',)
    fieldsets = (
        (None, {
            'fields': (
                'transaction_number', 'group', 'till', 'tax_free',
                'spacer','product_snapshot', 'payment_snapshot', 
                'final_price', 'final_gst', 'total', 'payment', 'change', 'receipt',
            )
        }),
    )
    inlines = [TransactionCurrencyInline, TransactionProductInline]

    def spacer(self, obj=None):
        return mark_safe('<div style="margin: 100px 0;"></div>')
    spacer.short_description = ''

    def product_snapshot(self, obj):
        items = obj.transactionproduct_set.select_related('product').all()
        if not items:
            return mark_safe("<p><em>No products on this transaction.</em></p>")

        html = ['<table style="width:100%; border-collapse: collapse;">',
                '<thead><tr>'
                '<th style="border:1px solid #ddd;padding:4px;">Product</th>'
                '<th style="border:1px solid #ddd;padding:4px;">Price</th>'
                '<th style="border:1px solid #ddd;padding:4px;">Discount %</th>'
                '<th style="border:1px solid #ddd;padding:4px;">Qty</th>'
                '<th style="border:1px solid #ddd;padding:4px;">Final Price</th>'
                '<th style="border:1px solid #ddd;padding:4px;">Final GST</th>'
                '<th style="border:1px solid #ddd;padding:4px;">Total</th>'
                '</tr></thead><tbody>']

        for i in items:
            html.append(
                "<tr>"
                f"<td style='border:1px solid #eee;padding:4px;'>{i.product.name}</td>"
                f"<td style='border:1px solid #eee;padding:4px;text-align:right;'>{i.price:.2f}</td>"
                f"<td style='border:1px solid #eee;padding:4px;text-align:right;'>{i.discount_rate:.2f}</td>"
                f"<td style='border:1px solid #eee;padding:4px;text-align:right;'>{i.quantity}</td>"
                f"<td style='border:1px solid #eee;padding:4px;text-align:right;'>{i.final_price:.2f}</td>"
                f"<td style='border:1px solid #eee;padding:4px;text-align:right;'>{i.final_gst:.2f}</td>"
                f"<td style='border:1px solid #eee;padding:4px;text-align:right;'>{i.total:.2f}</td>"
                "</tr>"
            )
        html.append("</tbody></table>")
        return format_html("".join(html))
    product_snapshot.short_description = "Purchased Products"

    def payment_snapshot(self, obj):
        items = obj.transactioncurrency_set.select_related('currency').all()
        if not items:
            return mark_safe("<p><em>No payment on this transaction.</em></p>")

        html = ['<table style="width:100%; border-collapse: collapse;">',
                '<thead><tr>'
                '<th style="border:1px solid #ddd;padding:4px;">Currency</th>'
                '<th style="border:1px solid #ddd;padding:4px;">Payment</th>'
                '</tr></thead><tbody>']

        for i in items:
            html.append(
                "<tr>"
                f"<td style='border:1px solid #eee;padding:4px;'>{i.currency.name}</td>"
                f"<td style='border:1px solid #eee;padding:4px;text-align:right;'>{i.payment:.2f}</td>"
                "</tr>"
            )
        html.append("</tbody></table>")
        return format_html("".join(html))
    payment_snapshot.short_description = "Payment Currencies"


    ## add a empty page
