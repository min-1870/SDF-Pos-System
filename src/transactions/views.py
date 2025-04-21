from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .models import Currency
from .forms import CurrencyForm

class HomeView(TemplateView):
    template_name = 'groups/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currencies'] = Currency.objects.all()
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