from django.contrib.auth.forms import UserCreationForm
from .models import Utente

class RegistrazioneForm(UserCreationForm):
    class Meta:
        model = Utente  
        fields = ['username', 'ruolo']  
