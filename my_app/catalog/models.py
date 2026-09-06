from django.db import models
from django.conf import settings
from django.db.models import Avg
from decimal import Decimal
from django.core.validators import MinValueValidator

# Create your models here.
class Categoria(models.Model):
    CATEGORIA = [
        ('sneakers','Sneakers'),
        ('running','Running'),
        ('eleganti','Eleganti'),
        ('stivali', 'Stivali'),
        ('sandali','Sandali')
    ]

    nome = models.CharField(max_length=20, choices=CATEGORIA)

    class Meta:
        verbose_name_plural = 'Categorie'

    def __str__(self):
        return self.nome

class Prodotto(models.Model):
    TAGLIE_DISPONIBILI = []
    for taglia in range(35,46):
        TAGLIE_DISPONIBILI.append((Decimal(f"{taglia}.0"), str(taglia)))
        TAGLIE_DISPONIBILI.append((Decimal(f"{taglia}.5"), f"{taglia}.5"))
        
    nome = models.CharField(max_length=50)
    immagine = models.ImageField(upload_to='prodotti_img/')
    taglia = models.DecimalField(max_digits=3,decimal_places=1, choices=TAGLIE_DISPONIBILI)
    prezzo = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    descrizione = models.TextField(max_length=300, default='Nessuna descrizione.')
    disponibile = models.BooleanField(default=True)
    pubblicazione = models.DateTimeField(auto_now_add=True)

    venditore = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    class Meta: 
        verbose_name_plural = 'Prodotti'

    def valutazione_media(self):
        recensioni = self.recensioni.all()
        if not recensioni: 
            return "Nessuna recensione"
        else:
            risultato = recensioni.aggregate(Avg('valutazione'))
            return risultato['valutazione__avg']

    def __str__(self):
        return f"{self.nome} (Taglia: {self.taglia} - Prezzo: €{self.prezzo})"