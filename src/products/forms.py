from django import forms
from .models import Brand, Product, Bundle, Barcode

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


from django import forms
from django.forms import inlineformset_factory
from .models import Bundle, Barcode, ProductBundle


class BundleForm(forms.ModelForm):
    # This goes in forms.py
    barcode_value = forms.CharField(
        label="Barcode",
        max_length=50,
        help_text="Enter a unique barcode for the bundle"
    )

    class Meta:
        model = Bundle
        # Exclude the FK, use barcode_value instead
        fields = ['name', 'description', 'price', 'discount_rate', 'barcode_value']

    def save(self, commit=True):
        # Create or get Barcode, assign to bundle
        bundle = super().save(commit=False)
        code = self.cleaned_data['barcode_value']
        barcode_obj, created = Barcode.objects.get_or_create(barcode=code)
        bundle.barcode = barcode_obj
        if commit:
            bundle.save()
        return bundle

# Inline formset for ProductBundle
ProductBundleFormSet = inlineformset_factory(
    parent_model=Bundle,
    model=ProductBundle,
    fields=('product', 'quantity'),
    extra=1,
    can_delete=True
)

class ProductForm(forms.ModelForm):
    # override the FK field with a simple CharField
    barcode_value = forms.CharField(
        label="Barcode",
        max_length=50,
        # help_text="Enter a unique barcode string"
    )

    class Meta:
        model = Product
        # note: *do not* include the original `barcode` FK field
        fields = [
            "name", "description", "price",
            "discount_rate", "tax_rate", "count",
            "barcode_value", "brand",
        ]

    def save(self, commit=True):
        # first, save the Product instance (without setting barcode)
        product = super().save(commit=False)

        code = self.cleaned_data["barcode_value"]
        # create or get the Barcode (you could also just create())
        barcode_obj, created = Barcode.objects.get_or_create(barcode=code)

        product.barcode = barcode_obj
        if commit:
            product.save()
        return product