from django import forms
from django.forms import CheckboxSelectMultiple
from django.utils.html import format_html

from product.models import Sale, Product


class ProductsField(forms.Field):
    pass


class ColoredCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = "django/forms/widgets/tags_checkbox.html"
    option_template_name = "django/forms/widgets/tags_checkbox_option.html"

    def create_option(
            self, *args, **kwargs
    ):
        result = super().create_option(*args, **kwargs)
        tag = args[1].instance
        if tag_color := tag.color:
            result['attrs']['label'] = {}
            result['attrs']['label']['style'] = (f'background-color: {tag_color};'
                                                 f' margin-top: 5px;border-radius: 10px;'
                                                 f'padding-left: 5px')

        return result

    def get_context(self, name, value, attrs):
        result = super().get_context(name, value, attrs)
        return result


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'tags': ColoredCheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)

        print(args, kwargs)
        if False:
            self.fields['amount_to_notify'].widget = forms.HiddenInput()
            self.fields['type'].widget = forms.HiddenInput()
            self.fields['hidden'].widget = forms.HiddenInput()
            self.fields['order'].widget = forms.HiddenInput()
            self.fields['payment_link'].widget = forms.HiddenInput()
            self.fields['remaining'].widget = forms.HiddenInput()
            self.fields['provider_purchase_date'].widget = forms.HiddenInput()


class SaleInlineForm(forms.ModelForm):

    receipt_products = forms.CharField(max_length=10000, label='Receipt Products', widget=forms.Textarea(attrs={'rows': 10, 'cols': 45}))


    class Meta:
        model = Sale
        exclude = ("products", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            # Set the custom value based on the parent object (obj)
            self.initial['receipt_products'] = self._receipt_products(self.instance)

    def format_product_string(self, product: Product):
        return f"{str(product)} - {product.console_type} - ₡{product.payment.net_price if product.payment else self.instance.net_total} - {product.owner} - ID: {product.id} \n"

    def _receipt_products(self, obj: Sale):
        products_string = [ self.format_product_string(product) for product in obj.products.all() ]
        return " ".join(products_string)
