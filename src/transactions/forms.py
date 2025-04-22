from django import forms
from .models import Currency, Till

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

# class GuideForm(forms.ModelForm):
#     class Meta:
#         model = Guide
#         fields = '__all__'

# class GroupTypeForm(forms.ModelForm):
#     class Meta:
#         model = GroupType
#         fields = '__all__'

# class GroupForm(forms.ModelForm):
#     class Meta:
#         model = Group
#         fields = '__all__'
#         widgets = {
#             'date': forms.DateInput(
#                 attrs={
#                   'type': 'date',
#                   'class': 'form-control',
#                 },
#                 format='%Y-%m-%d'
#             ),
#         }
