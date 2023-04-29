from django import forms
from .models import Pojistenec, Uzivatel, Detail_pojisteni

class PojistenecForm(forms.ModelForm):
    detail_pojisteni = forms.ModelMultipleChoiceField(queryset = Detail_pojisteni.objects.all(), required = False)
	
    class Meta:
        model = Pojistenec
        fields=["jmeno", "prijmeni","vek", "adresa", "pojisteni", "detail_pojisteni"]
		
class UzivatelForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = Uzivatel
        fields = ["email", "password"]
		
class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
