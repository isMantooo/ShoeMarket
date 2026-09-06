from django.db import models
from django.contrib.auth.models import AbstractUser 

class Utente(AbstractUser):
    RUOLO = [
        ('acquirente','Acquirente'),    
        ('venditore','Venditore'),
    ]
    ruolo = models.CharField(max_length=12, choices=RUOLO, default='acquirente')

    class Meta:
        verbose_name_plural = 'Utenti'
