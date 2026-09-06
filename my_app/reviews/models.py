from django.db import models
from django.conf import settings
from catalog.models import Prodotto

# Create your models here.
class Recensione(models.Model):
    VALUTAZIONE = [
        (1,'1 stella'),
        (2,'2 stelle'),
        (3,'3 stelle'),
        (4,'4 stelle'),
        (5,'5 stelle'),
    ]

    valutazione = models.IntegerField(choices=VALUTAZIONE)
    commento = models.TextField(max_length=300, blank=True)
    data = models.DateField(auto_now_add=True)

    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, related_name='recensioni')
    acquirente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('prodotto', 'acquirente')
        verbose_name_plural = 'Recensioni'

    def __str__(self):
        return f"Recensione di {self.acquirente.username} (Prodotto: {self.prodotto.nome})"
