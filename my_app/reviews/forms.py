from django import forms
from .models import Recensione

class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = ['valutazione','commento']