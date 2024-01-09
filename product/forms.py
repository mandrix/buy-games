from django import forms

from product.models import Sale

class ProductsField(forms.Field):
    pass


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

    @staticmethod
    def format_product_string(product):
        return f"{str(product)} - ₡{product.payment.net_price} - {product.owner} - {product.barcode} - ID: {product.id} \n"

    def _receipt_products(self, obj: Sale):
        products_string = [ self.format_product_string(product) for product in obj.products.all() ]
        return " ".join(products_string)
