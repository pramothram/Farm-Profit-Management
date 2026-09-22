from django import forms
from .models import Farm,Expense, Harvest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

class FarmForm(forms.ModelForm):

    class Meta:
        model = Farm

        fields = [
            'crop_name',
            'land_size',
            'land_unit',
            'planting_date',
            'expected_harvest_date',
            'location',
        ]

        widgets = {

            'crop_name': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Paddy'
                }
            ),

            'land_size': forms.NumberInput(
                attrs={
                    'placeholder': 'Example: 2',
                    'step': '0.01'
                }
            ),

            'planting_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'expected_harvest_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Village / District'
                }
            ),
        }

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense

        fields = [
            'date',
            'purpose',
            'amount',
            'notes',
        ]

        widgets = {

            'date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'purpose': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Fertilizer'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'placeholder': 'Example: 2500',
                    'step': '0.01'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'placeholder': 'Enter additional details...',
                    'rows': 4
                }
            ),
        }

class HarvestForm(forms.ModelForm):

    class Meta:
        model = Harvest

        fields = [
            'date',
            'quantity',
            'unit',
            'selling_price',
            'notes',
        ]

        widgets = {

            'date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'placeholder': 'Example: 2000',
                    'step': '0.01',
                    'min': '0'
                }
            ),

            'unit': forms.TextInput(
                attrs={
                    'placeholder': 'Example: kg'
                }
            ),

            'selling_price': forms.NumberInput(
                attrs={
                    'placeholder': 'Example: 35',
                    'step': '0.01',
                    'min': '0'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'placeholder': 'Enter additional details...',
                    'rows': 4
                }
            ),
        }