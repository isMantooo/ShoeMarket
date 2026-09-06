from django.db import models
from django.conf import settings
from catalog.models import Prodotto

# Create your models here.
class Preferito(models.Model):
    data_aggiunta = models.DateField(auto_now_add=True)

    acquirente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('prodotto', 'acquirente')
        verbose_name_plural = 'Preferiti'

    def __str__(self):
        return f"Preferiti di {self.acquirente.username}"