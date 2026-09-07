from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Ordine 
from catalog.models import Prodotto

# Create your views here.
def ordine_view(request, pk):
    if not(request.user.is_authenticated and request.user.ruolo == 'acquirente'):
        messages.error(request, "Devi accedere come 'acquirente' per poter acquistare un prodotto!")
        return redirect('catalogo')

    prodotto = get_object_or_404(Prodotto, pk=pk)

    Ordine.objects.create(prodotto=prodotto, acquirente=request.user)

    prodotto.disponibile = False
    prodotto.save()
    messages.success(request, "Acquisto effettuato con successo!")

    return redirect('catalogo')

def storico_ordini(request):
    if not(request.user.is_authenticated and request.user.ruolo == 'acquirente'):
        return redirect('catalogo')

    lista_ordini = Ordine.objects.filter(acquirente=request.user).order_by('-data_acquisto')

    return render(request, 'orders/storico_ordini_template.html', {'ordini': lista_ordini})