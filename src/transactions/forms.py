# transactions/forms.py

from decimal import Decimal
from django import forms
from .models import TransactionProduct, TransactionCurrency

class TransactionCurrencyInlineForm(forms.ModelForm):
    remain = forms.DecimalField(
        label='Remain',
        required=False,
        disabled=True,
        initial=0
    )

    class Meta:
        model   = TransactionCurrency
        fields  = ('currency', 'payment', 'remain')
        exclude = ('transaction',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        transaction = getattr(self.instance, 'transaction', None)
        total = transaction.total if transaction else 0

        # default amount
        self.fields['payment'].initial = 0

        # Set remain field value
        remain_value = 0
        if getattr(self.instance, 'currency', None) and hasattr(self.instance.currency, 'currency_rate'):
            tc_queryset = TransactionCurrency.objects.filter(transaction=self.instance.transaction)
            received_amount = sum(tc.payment / tc.currency.currency_rate for tc in tc_queryset)
            remain_value = (total - received_amount) * self.instance.currency.currency_rate
        self.fields['remain'].initial = round(remain_value, 2)


class TransactionProductInlineForm(forms.ModelForm):
    class Meta:
        model   = TransactionProduct
        fields = ('total', 'final_gst', 'product', 'promotion', 'quantity', 'price', 'discount_rate')
        exclude = ('transaction','final_price', )
        widgets = {
            'total': forms.TextInput(attrs={'readonly': 'readonly'}),
            'final_price': forms.TextInput(attrs={'readonly': 'readonly'}),
            'final_gst': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # default quantity
        self.fields['quantity'].initial = 1
        