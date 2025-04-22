from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .models import Currency, Till, Transaction, TransactionCurrency, TransactionProduct, TransactionBundle
from .forms import CurrencyForm, TillForm

class HomeView(TemplateView):
    template_name = 'transactions/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currencies'] = Currency.objects.all()
        context['tills'] = Till.objects.all()
        return context
    
# Create your views here.
class CurrencyListView(ListView):
    model = Currency
    template_name = 'transactions/currency_list.html'

class CurrencyCreateView(CreateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'transactions/currency_form.html'
    success_url = reverse_lazy('currency_list')

class CurrencyUpdateView(UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'transactions/currency_form.html'
    success_url = reverse_lazy('currency_list')
    


class TillListView(ListView):
    model = Till
    template_name = 'transactions/till_list.html'

class TillCreateView(CreateView):
    model = Till
    form_class = TillForm
    template_name = 'transactions/till_form.html'
    success_url = reverse_lazy('till_list')

class TillUpdateView(UpdateView):
    model = Till
    form_class = TillForm
    template_name = 'transactions/till_form.html'
    success_url = reverse_lazy('till_list')