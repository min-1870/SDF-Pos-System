
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .models import Company, Guide, GroupType, Group
from .forms import CompanyForm, GuideForm, GroupTypeForm, GroupForm
# from django.views.generic.edit import FormView

from django.contrib import admin
from django.template.response import TemplateResponse
from products.models import Product

from django.db.models import Subquery, OuterRef, Sum
from transactions.models import TransactionProduct
# class CustomAdminSite(admin.AdminSite):
#     site_header = "My Admin"

#     def index(self, request, extra_context=None):
#         # get all products
#         qs = Product.order_by('-price')
#         labels = [p.name for p in qs]
#         data   = [float(p.price) for p in qs]

#         extra_context = extra_context or {}
#         extra_context['chart_labels'] = labels
#         extra_context['chart_data']   = data

#         # sold quantity
        
#         qs = Product.objects.annotate(
#             total=Subquery(
#                 TransactionProduct.objects.filter(product=OuterRef('pk'))
#                 .values('product')
#                 .annotate(sold=Sum('quantity'))
#                 .values('sold')[:1]
#             )
#         ).order_by('-total')
#         sold_labels = [p.name for p in qs]
#         sold_data   = [float(p.total) if p.total is not None else 0 for p in qs]
#         extra_context['sold_chart_labels'] = sold_labels
#         extra_context['sold_chart_data']   = sold_data

#         return TemplateResponse(request, "admin/index.html", extra_context)

# # Use the custom site
# custom_admin_site = CustomAdminSite(name='custom_admin')

# from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from products.models import Product


# def custom_admin_dashboard(request):
#         qs = Product.order_by('-price')
#         labels = [p.name for p in qs]
#         data   = [float(p.price) for p in qs]

#         extra_context = extra_context or {}
#         extra_context['chart_labels'] = labels
#         extra_context['chart_data']   = data

#         # sold quantity
        
#         qs = Product.objects.annotate(
#             total=Subquery(
#                 TransactionProduct.objects.filter(product=OuterRef('pk'))
#                 .values('product')
#                 .annotate(sold=Sum('quantity'))
#                 .values('sold')[:1]
#             )
#         ).order_by('-total')
#         sold_labels = [p.name for p in qs]
#         sold_data   = [float(p.total) if p.total is not None else 0 for p in qs]
#         extra_context['sold_chart_labels'] = sold_labels
#         extra_context['sold_chart_data']   = sold_data

#         return render(request, 'admin/index.html', extra_context)
