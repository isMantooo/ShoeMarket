from django.shortcuts import render, redirect
from collections import Counter
from .models import Ricerca
from favorites.models import Preferito
from orders.models import Ordine
from catalog.models import Prodotto

# Create your views here.
def consigliati_view(request):
    if not request.user.is_authenticated:
        return redirect('catalogo')

    categorie_preferiti = Preferito.objects.filter(acquirente=request.user).values_list('prodotto__categoria__nome', flat=True)
    categorie_ordini = Ordine.objects.filter(acquirente=request.user).values_list('prodotto__categoria__nome', flat=True)
    categorie_tot = list(categorie_preferiti) + list(categorie_ordini)

    conteggio_c = Counter(categorie_tot)
    best_categoria = conteggio_c.most_common(1)
    categoria_scelta = best_categoria[0][0] if best_categoria else None

    taglie_preferiti = Preferito.objects.filter(acquirente=request.user).values_list('prodotto__taglia', flat=True)
    taglie_ordini = Ordine.objects.filter(acquirente=request.user).values_list('prodotto__taglia', flat=True)
    taglie_tot = list(taglie_preferiti) + list(taglie_ordini)

    conteggio_t = Counter(taglie_tot)
    best_taglia = conteggio_t.most_common(1)
    taglia_scelta = best_taglia[0][0] if best_taglia else None

    if not categoria_scelta:
        categorie_ricerche = Ricerca.objects.filter(acquirente=request.user).exclude(categoria='').exclude(categoria__isnull=True).values_list('categoria', flat=True)
        conteggio_rc = Counter(categorie_ricerche)
        best_ricerca_c = conteggio_rc.most_common(1)
        if best_ricerca_c:
            categoria_scelta = best_ricerca_c[0][0]

    if not taglia_scelta:
        taglie_ricerche = Ricerca.objects.filter(acquirente=request.user).exclude(taglia__isnull=True).values_list('taglia', flat=True)
        conteggio_rt = Counter(taglie_ricerche)
        best_ricerca_t = conteggio_rt.most_common(1)
        if best_ricerca_t:
            taglia_scelta = best_ricerca_t[0][0]

    if not categoria_scelta and not taglia_scelta:
        consigliati = Prodotto.objects.none()
    else:
        consigliati_categoria = Prodotto.objects.none()
        if categoria_scelta:
            consigliati_categoria = Prodotto.objects.filter(disponibile=True, categoria__nome=categoria_scelta)

        consigliati_taglia = Prodotto.objects.none()
        if taglia_scelta:
            consigliati_taglia = Prodotto.objects.filter(disponibile=True, taglia=taglia_scelta)

        id_categoria = list(consigliati_categoria.values_list('id', flat=True))
        id_taglia = list(consigliati_taglia.values_list('id', flat=True))
        id_uniti = list(set(id_categoria + id_taglia))

        consigliati = Prodotto.objects.filter(id__in=id_uniti)

        prodotti_preferiti_id = Preferito.objects.filter(acquirente=request.user).values_list('prodotto__id', flat=True)
        prodotti_ordinati_id = Ordine.objects.filter(acquirente=request.user).values_list('prodotto__id', flat=True)
        consigliati = consigliati.exclude(id__in=list(prodotti_preferiti_id) + list(prodotti_ordinati_id))

    return render(request, 'recommendations/consigliati_template.html', {'prodotti': consigliati})