from django.db import models
from django.conf import settings

# Create your models here.
class Ricerca(models.Model):
    categoria = models.CharField(max_length=15 ,blank=True, null=True)
    prezzo_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    prezzo_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    taglia = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    data = models.DateField(auto_now_add=True)

    acquirente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Consigliati'

    def __str__(self):
        return f"Consigliati di {self.acquirente.username}"