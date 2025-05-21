from django import forms
from .models import Currency, Till, Transaction, TransactionItem, TransactionCurrency
from products.models import Bundle, Product
from django.forms.models import inlineformset_factory
from django.contrib.contenttypes.models import ContentType

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = '__all__'    


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['group','till','tax_free']

class TransactionCurrencyForm(forms.ModelForm):
    class Meta:
        model = TransactionCurrency
        fields = '__all__'

TransactionCurrencyFormSet = inlineformset_factory(
    parent_model=Transaction,
    model=TransactionCurrency,   # ← CORRECT: TransactionCurrency has the FK
    form=TransactionCurrencyForm,
    extra=1,
    can_delete=False
)
    
class TransactionItemForm(forms.ModelForm):
    ITEM_CHOICES = [
        (f"prod_{p.pk}", p.name) for p in Product.objects.all()
    ] + [
        (f"bund_{b.pk}", f"{b.name} (bundle)") for b in Bundle.objects.all()
    ]

    item_choice = forms.ChoiceField(
        choices=ITEM_CHOICES,
        label="Item"
    )
    class Meta:
        model = TransactionItem
        fields = ['item_choice', 'custom_price', 'custom_discount_rate', 'quantity']

    def save(self, commit=True):
        inst = super().save(commit=False)
        kind, pk = self.cleaned_data['item_choice'].split('_', 1)
        if kind == 'prod':
            inst.content_type = ContentType.objects.get_for_model(Product)
        else:
            inst.content_type = ContentType.objects.get_for_model(Bundle)
        inst.object_id = pk
        if commit:
            inst.save()
        return inst

TransactionItemFormSet = inlineformset_factory(
    Transaction, TransactionItem,
    form=TransactionItemForm,
    extra=1, can_delete=True
)


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(
                attrs={
                  'type': 'date',
                  'class': 'form-control',
                },
                format='%Y-%m-%d'
            ),
        }

class TillForm(forms.ModelForm):
    class Meta:
        model = Till
        fields = '__all__'
