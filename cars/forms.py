# cars/forms.py

from django import forms
from .models import Car, Sale, VehicleDocument, VehicleDocumentImage, AppConfiguration


class CarForm(forms.ModelForm):
    class Meta:
        def clean_money_value(self, field_name):
            value = self.cleaned_data.get(field_name)

            if value in [None, '']:
                return 0

            if isinstance(value, str):
                value = value.replace('.', '').replace(',', '.')

                return value

        def clean_purchase_price(self):
            return self.clean_money_value('purchase_price')

        def clean_sale_price(self):
            return self.clean_money_value('sale_price')

        def clean_fipe_initial_price(self):
            return self.clean_money_value('fipe_initial_price')

        def clean_fipe_current_price(self):
            return self.clean_money_value('fipe_current_price')

        model = Car
        fields = [
            'brand',
            'model',
            'year',
            'plate',
            'color',
            'mileage',
            'purchase_price',
            'sale_price',
            'status',
            'publication_sites',
            'image',

            'needs_cleaning',
            'needs_sanitizing',
            'has_spare_key',
            'has_cautelar',
            'has_procuracao',
            'has_crlv',

            'ad_olx',
            'ad_webmotors',
            'ad_icarros',
            'ad_mercado_livre',
            'ad_facebook',
            'ad_instagram',
            'other_ad_sites',

            'fipe_code',
            'fipe_initial_price',
            'fipe_current_price',

            'observations',
        ]

        widgets = {
            'brand': forms.TextInput(attrs={
                'placeholder': 'Selecione a marca',
                'class': 'form-control'
            }),
            'model': forms.TextInput(attrs={
                'placeholder': 'Selecione o modelo',
                'class': 'form-control'
            }),
            'year': forms.NumberInput(attrs={
                'placeholder': 'Ano',
                'class': 'form-control'
            }),
            'plate': forms.TextInput(attrs={
                'placeholder': 'ABC-1234',
                'class': 'form-control'
            }),
            'color': forms.TextInput(attrs={
                'placeholder': 'Branco',
                'class': 'form-control'
            }),
            'mileage': forms.NumberInput(attrs={
                'placeholder': '50000',
                'class': 'form-control'
            }),
            'purchase_price': forms.TextInput(attrs={
                'placeholder': '40.000,00',
                'class': 'form-control money-input'
            }),
            'sale_price': forms.TextInput(attrs={
                'placeholder': '50.000,00',
                'class': 'form-control money-input'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'publication_sites': forms.TextInput(attrs={
                'placeholder': 'Ex: OLX, WebMotors...',
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'fipe_code': forms.TextInput(attrs={
                'placeholder': 'Ex: 004219-1',
                'class': 'form-control'
            }),
            'fipe_initial_price': forms.TextInput(attrs={
                'placeholder': '50.000,00',
                'class': 'form-control money-input',
                'id': 'fipe_initial_price'
            }),
            'fipe_current_price': forms.TextInput(attrs={
                'placeholder': '45.000,00',
                'class': 'form-control money-input',
                'id': 'fipe_current_price'
            }),
            
            'ad_olx': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
            'ad_webmotors': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
            'ad_icarros': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
            'ad_mercado_livre': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
            'ad_facebook': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
            'ad_instagram': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),

            'other_ad_sites': forms.TextInput(attrs={
                'placeholder': 'Nome do site...',
                'class': 'form-control'
            }),

            'observations': forms.Textarea(attrs={
                'placeholder': 'Adicione observações sobre o veículo, manutenções, documentação, histórico, etc...',
                'class': 'form-control observations-textarea',
            }),

            'needs_cleaning': forms.Select(attrs={'class': 'form-control'}),
            'needs_sanitizing': forms.Select(attrs={'class': 'form-control'}),
            'has_spare_key': forms.Select(attrs={'class': 'form-control'}),
            'has_cautelar': forms.Select(attrs={'class': 'form-control'}),
            'has_procuracao': forms.Select(attrs={'class': 'form-control'}),
            'has_crlv': forms.Select(attrs={'class': 'form-control'}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale

        fields = [
            'car',
            'sale_date',
            'sale_price',
            'payment_method',
            'buyer_type',
            'buyer_name',
            'cpf',
            'rg',
            'address',
            'phone',
            'email',
            'observations',
        ]

        widgets = {
            'car': forms.Select(attrs={
                'class': 'form-control'
            }),

            'sale_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'sale_price': forms.TextInput(attrs={
                'placeholder': '50000',
                'class': 'form-control money-input'
            }),

            'payment_method': forms.TextInput(attrs={
                'placeholder': 'Ex: À vista, Financiamento, etc.',
                'class': 'form-control'
            }),

            'buyer_type': forms.RadioSelect(choices=Sale.BUYER_TYPE_CHOICES),

            'buyer_name': forms.TextInput(attrs={
                'placeholder': 'João da Silva',
                'class': 'form-control'
            }),

            'cpf': forms.TextInput(attrs={
                'placeholder': '000.000.000-00',
                'class': 'form-control'
            }),

            'rg': forms.TextInput(attrs={
                'placeholder': '00.000.000-0',
                'class': 'form-control'
            }),

            'address': forms.TextInput(attrs={
                'placeholder': 'Rua, número, bairro, cidade',
                'class': 'form-control'
            }),

            'phone': forms.TextInput(attrs={
                'placeholder': '(00) 00000-0000',
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'email@exemplo.com',
                'class': 'form-control'
            }),

            'observations': forms.Textarea(attrs={
                'placeholder': 'Observações sobre a venda...',
                'class': 'form-control textarea-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['car'].queryset = Car.objects.filter(status='estoque')
        self.fields['car'].empty_label = 'Selecione o carro'

    def clean_sale_price(self):
        value = self.cleaned_data.get('sale_price')

        if value in [None, '']:
            return 0

        if isinstance(value, str):
            value = value.replace('.', '').replace(',', '.')

        return value

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={
            "multiple": True,
            "class": "form-control"
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [super(MultipleFileField, self).clean(file, initial) for file in data]

        return [super().clean(data, initial)]


class VehicleDocumentForm(forms.ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = VehicleDocument
        fields = [
            'car',
            'document_type',
            'name',
            'notes',
            'images',
        ]

        widgets = {
            'car': forms.Select(attrs={
                'class': 'form-control'
            }),
            'document_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: CRLV_2026',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Adicione observações sobre o documento...',
                'class': 'form-control textarea-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['car'].empty_label = 'Selecione o carro'
        self.fields['document_type'].empty_label = 'Selecione o tipo'


class AccessPasswordCreateForm(forms.Form):
    new_password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite uma senha de proteção',
            'class': 'form-control'
        })
    )


class CredentialsUnlockForm(forms.Form):
    access_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite a senha',
            'class': 'form-control'
        })
    )


class ItauCredentialsForm(forms.Form):
    itau_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@exemplo.com',
            'class': 'form-control'
        })
    )

    itau_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha do Itaú',
            'class': 'form-control'
        })
    )


class ChangeAccessPasswordForm(forms.Form):
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha atual',
            'class': 'form-control'
        })
    )

    new_password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite a nova senha',
            'class': 'form-control'
        })
    )
