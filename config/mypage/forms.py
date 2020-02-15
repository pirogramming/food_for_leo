from django import forms

from mypage.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['img']
