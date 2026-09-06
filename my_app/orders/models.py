from django.db import models
from catalog.models import Prodotto
from django.conf import settings

# Create your models here.
class Ordine(models.Model):
    stato = models.CharField(max_length=15 ,default='completato')
    data_acquisto = models.DateField(auto_now_add=True)

    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE)
    acquirente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Ordini'

    def __str__(self):
        return f"Ordine di {self.acquirente.username}"