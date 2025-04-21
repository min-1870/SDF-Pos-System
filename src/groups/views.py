
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .models import Company, Guide, GroupType, Group
from .forms import CompanyForm, GuideForm, GroupTypeForm, GroupForm
# from django.views.generic.edit import FormView

class HomeView(TemplateView):
    template_name = 'groups/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        context['guides'] = Guide.objects.all()
        context['groups'] = Group.objects.all()
        return context

class CompanyListView(ListView):
    model = Company
    template_name = 'groups/company_list.html'

class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'groups/company_form.html'
    success_url = reverse_lazy('company_list')

class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'groups/Company_form.html'
    success_url = reverse_lazy('company_list')

# -- Product Views --
class GuideListView(ListView):
    model = Guide
    template_name = 'groups/guide_list.html'

class GuideCreateView(CreateView):
    model = Guide
    form_class = GuideForm
    template_name = "groups/guide_form.html"
    success_url = reverse_lazy("guide_list")

class GuideUpdateView(UpdateView):
    model = Guide
    form_class = GuideForm
    template_name = 'groups/guide_form.html'
    success_url = reverse_lazy('guide_list')

# -- Bundle Views --
class GroupTypeListView(ListView):
    model = GroupType
    template_name = 'groups/group_type_list.html'

class GroupTypeCreateView(CreateView):
    model = GroupType
    form_class = GroupTypeForm
    template_name = "groups/group_type_form.html"
    success_url = reverse_lazy("group_list")

class GroupTypeUpdateView(UpdateView):
    model = GroupType
    form_class = GroupTypeForm
    template_name = 'groups/group_type_form.html'
    success_url = reverse_lazy('group_type_list')

# -- Bundle Views --
class GroupListView(ListView):
    model = Group
    template_name = 'groups/group_list.html'

class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = "groups/group_form.html"
    success_url = reverse_lazy("group_list")

class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'groups/group_form.html'
    success_url = reverse_lazy('group_list')

# from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
# from django.views import View
# from .forms import BundleForm, ProductBundleFormSet


# class BundleCreateView(View):
#     # Place this in views.py
#     template_name = 'products/bundle_form.html'
#     success_url = reverse_lazy('bundle_list')

#     def get(self, request, *args, **kwargs):
#         form = BundleForm()
#         formset = ProductBundleFormSet()
#         return render(request, self.template_name, {'form': form, 'formset': formset})

#     def post(self, request, *args, **kwargs):
#         form = BundleForm(request.POST)
#         formset = ProductBundleFormSet(request.POST)
#         if form.is_valid() and formset.is_valid():
#             bundle = form.save()
#             # Associate formset with the new bundle
#             formset.instance = bundle
#             formset.save()
#             return redirect(self.success_url)
#         return render(request, self.template_name, {'form': form, 'formset': formset})

# class BundleUpdateView(UpdateView):
#     model = Bundle
#     form_class = BundleForm
#     template_name = 'products/bundle_form.html'
#     success_url = reverse_lazy('bundle_list')