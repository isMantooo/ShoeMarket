from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages
from .models import Prodotto, Categoria
from .forms import ProdottoForm
from favorites.models import Preferito
from orders.models import Ordine
from recommendations.models import Ricerca

# Create your views here.
def catalogo_view(request):
    lista_scarpe = Prodotto.objects.filter(disponibile=True).order_by('-pubblicazione')

    categoria_filtro = request.GET.get('categoria')
    if categoria_filtro:
        lista_scarpe = lista_scarpe.filter(categoria__nome=categoria_filtro)

    taglia_filtro = request.GET.get('taglia')
    if taglia_filtro:
        lista_scarpe = lista_scarpe.filter(taglia=taglia_filtro)

    prezzo_min = request.GET.get('prezzo_min')
    prezzo_max = request.GET.get('prezzo_max')

    if prezzo_min:
        try:
            prezzo_min = float(prezzo_min)
            if prezzo_min < 0:
                messages.error(request, "Il prezzo minimo non può essere negativo.")
            else:
                lista_scarpe = lista_scarpe.filter(prezzo__gte=prezzo_min)
        except ValueError:
            messages.error(request, "Il prezzo minimo inserito non è valido.")

    if prezzo_max:
        try:
            prezzo_max = float(prezzo_max)
            if prezzo_max < 0:
                messages.error(request, "Il prezzo massimo non può essere negativo.")
            else:
                lista_scarpe = lista_scarpe.filter(prezzo__lte=prezzo_max)
        except ValueError:
            messages.error(request, "Il prezzo massimo inserito non è valido.") 

    ricerca_filtro = request.GET.get('ricerca')
    if ricerca_filtro:
        lista_scarpe = lista_scarpe.filter(nome__icontains=ricerca_filtro)

    if request.user.is_authenticated:
        if (categoria_filtro or taglia_filtro or prezzo_max or prezzo_min):
            Ricerca.objects.create(acquirente=request.user, categoria=categoria_filtro, prezzo_min=prezzo_min or None, prezzo_max=prezzo_max or None, taglia=taglia_filtro or None)
    
    return render(request, 'catalog/catalogo_template.html', {'prodotti': lista_scarpe, 'categoria': Categoria.CATEGORIA, 'taglia': Prodotto.TAGLIE_DISPONIBILI})

def crea_prodotto(request):
    if not(request.user.is_authenticated and request.user.ruolo == 'venditore'):
        return redirect('catalogo')

    if request.method == 'POST':
        form = ProdottoForm(request.POST, request.FILES)
        if form.is_valid():
            prodotto = form.save(commit=False)
            prodotto.venditore = request.user
            prodotto.save()
            messages.success(request, "Prodotto creato con successo!")
            return redirect('catalogo')
    else:
        form = ProdottoForm()

    return render(request, 'catalog/prodform_template.html', {'form' : form})

def dettagli_prodotto(request, pk):
    prodotto = get_object_or_404(Prodotto, pk=pk)

    preferito_y = False
    if request.user.is_authenticated:
        preferito_y = Preferito.objects.filter(acquirente=request.user, prodotto=prodotto).exists()

    return render(request, 'catalog/prodotto_template.html', {'prodotto': prodotto,'preferito_y': preferito_y})

def venditore_view(request):
    if not (request.user.is_authenticated and request.user.ruolo == 'venditore'):
        return redirect('catalogo')
    
    lista_scarpe = Prodotto.objects.filter(venditore=request.user).order_by('-disponibile','-pubblicazione')

    ordini = Ordine.objects.filter(prodotto__venditore=request.user)
    ordini_tot = ordini.count()

    risultato = ordini.aggregate(Sum('prodotto__prezzo', default=0))
    guadagno_tot = risultato['prodotto__prezzo__sum']

    
    return render(request, 'catalog/venditore_template.html', {'prodotti': lista_scarpe, 'ordini_tot': ordini_tot, 'guadagno_tot': guadagno_tot})
    
def rimuovi_prodotto(request, pk):
    prodotto = get_object_or_404(Prodotto, pk=pk)
    
    if not (request.user.is_authenticated and request.user == prodotto.venditore):
        return redirect('catalogo')
    
    if not prodotto.disponibile:
        messages.error(request, "Non puoi rimuovere un prodotto già venduto.")
        return redirect('venditore')
    
    prodotto.delete()
    messages.success(request, "Prodotto rimosso con successo.")
    return redirect('venditore')