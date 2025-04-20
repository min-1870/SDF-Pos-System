
from django.urls import path
from .views import (
    HomeView,
    BrandListView, BrandCreateView, BrandUpdateView,
    ProductListView, ProductCreateView, ProductUpdateView,
    BundleListView, BundleCreateView, BundleUpdateView,
)

urlpatterns = [
    # Home / Dashboard
    path('', HomeView.as_view(), name='home'),
    # Brand CRUD
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/add/', BrandCreateView.as_view(), name='brand_add'),
    path('brands/edit/<int:pk>/', BrandUpdateView.as_view(), name='brand_edit'),

    # Product CRUD
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),

    # Bundle CRUD
    path('bundles/', BundleListView.as_view(), name='bundle_list'),
    path('bundles/add/', BundleCreateView.as_view(), name='bundle_add'),
    path('bundles/edit/<int:pk>/', BundleUpdateView.as_view(), name='bundle_edit'),
]