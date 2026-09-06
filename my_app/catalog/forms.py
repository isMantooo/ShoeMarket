from django import forms 
from .models import Prodotto

class ProdottoForm(forms.ModelForm):
    class Meta:
        model = Prodotto
        fields = ['nome','immagine','taglia','prezzo','descrizione','categoria']