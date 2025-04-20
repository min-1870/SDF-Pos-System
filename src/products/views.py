
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .models import Brand, Product, Bundle
from .forms import BrandForm, ProductForm, BundleForm
from django.views.generic.edit import FormView
from .models import Barcode
from .forms import ProductForm

class HomeView(TemplateView):
    template_name = 'products/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['products'] = Product.objects.all()
        context['bundles'] = Bundle.objects.all()
        return context

class BrandListView(ListView):
    model = Brand
    template_name = 'products/brand_list.html'

class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('brand_list')

class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_form.html'
    success_url = reverse_lazy('brand_list')

# -- Product Views --
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

# -- Bundle Views --
class BundleListView(ListView):
    model = Bundle
    template_name = 'products/bundle_list.html'

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import BundleForm, ProductBundleFormSet


class BundleCreateView(View):
    # Place this in views.py
    template_name = 'products/bundle_form.html'
    success_url = reverse_lazy('bundle_list')

    def get(self, request, *args, **kwargs):
        form = BundleForm()
        formset = ProductBundleFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = BundleForm(request.POST)
        formset = ProductBundleFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            bundle = form.save()
            # Associate formset with the new bundle
            formset.instance = bundle
            formset.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'formset': formset})

class BundleUpdateView(UpdateView):
    model = Bundle
    form_class = BundleForm
    template_name = 'products/bundle_form.html'
    success_url = reverse_lazy('bundle_list')