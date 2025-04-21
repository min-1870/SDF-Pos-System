from django.urls import path
from .views import (
    HomeView,
    CurrencyListView, CurrencyCreateView, CurrencyUpdateView,
    # CompanyListView, CompanyCreateView, CompanyUpdateView,
    # GuideListView, GuideCreateView, GuideUpdateView,
    # GroupTypeListView, GroupTypeCreateView, GroupTypeUpdateView,
    # GroupListView, GroupCreateView, GroupUpdateView,
)

urlpatterns = [
    # Home / Dashboard
    path('', HomeView.as_view(), name='home'),

    # Currency CRUD
    path('currencies/', CurrencyListView.as_view(), name='currency_list'),
    path('currencies/add/', CurrencyCreateView.as_view(), name='currency_add'),
    path('currencies/edit/<int:pk>/', CurrencyUpdateView.as_view(), name='currency_edit'),

    # # Company CRUD
    # path('company/', CompanyListView.as_view(), name='company_list'),
    # path('company/add/', CompanyCreateView.as_view(), name='company_add'),
    # path('company/edit/<int:pk>/', CompanyUpdateView.as_view(), name='company_edit'),

    # # Guide CRUD
    # path('guides/', GuideListView.as_view(), name='guide_list'),
    # path('guides/add/', GuideCreateView.as_view(), name='guide_add'),
    # path('guides/edit/<int:pk>/', GuideUpdateView.as_view(), name='guide_edit'),

    # # Group Type CRUD
    # path('group-types/', GroupTypeListView.as_view(), name='group_type_list'),
    # path('group-types/add/', GroupTypeCreateView.as_view(), name='group_type_add'),
    # path('group-types/edit/<int:pk>/', GroupTypeUpdateView.as_view(), name='group_type_edit'),

    # # Group CRUD
    # path('groups/', GroupListView.as_view(), name='group_list'),
    # path('groups/add/', GroupCreateView.as_view(), name='group_add'),
    # path('groups/edit/<int:pk>/', GroupUpdateView.as_view(), name='group_edit'),
]
