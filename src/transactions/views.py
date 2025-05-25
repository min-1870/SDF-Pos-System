from django.urls import reverse_lazy  #TODO fix the view to apply them w UI
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .models import Currency, Till, Transaction, TransactionCurrency, TransactionProduct, TransactionBundle
from .forms import CurrencyForm, TillForm, TransactionForm, TransactionItemFormSet, TransactionCurrencyFormSet
from django.shortcuts import render, redirect
from products.models import Product, Bundle

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'

class TransactionCreateView(CreateView):
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        product_list = list(Product.objects.all().values('id', 'name', 'price', 'discount_rate'))
        bundle_list = list(Bundle.objects.all().values('id', 'name', 'price', 'discount_rate'))
        currency_list = list(Currency.objects.all().values('id', 'name', 'currency_rate'))

        transaction = Transaction()
        item_formset = TransactionItemFormSet(instance=transaction, queryset=TransactionBundle.objects.none())
        currency_formset = TransactionCurrencyFormSet(instance=transaction)

        return render(request, self.template_name, {
            'form': form,
            'tif': item_formset,
            'currency_formset': currency_formset,
            'product_list': product_list,
            'bundle_list': bundle_list,
            'currency_list': currency_list,
        })

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        transaction_item_form_set = TransactionItemFormSet(request.POST)

        if form.is_valid() and transaction_item_form_set.is_valid():
            transaction = form.save(commit=False)
            transaction.receipt = "Test Receipt"
            transaction.save()
            for transaction_item in transaction_item_form_set:
                item = transaction_item.save(commit=False)
                item.transaction = transaction
                item.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'tif': transaction_item_form_set})
