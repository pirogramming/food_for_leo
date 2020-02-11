from dal import autocomplete

from django import forms

from core.models import Product, Mall, Brand


class MallForm(forms.ModelForm):
    Select_Brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        widget=autocomplete.ModelSelect2(url='search_autocomplete')
    )

    class Meta:
        model = Mall
        fields = ('__all__')