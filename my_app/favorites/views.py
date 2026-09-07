from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Preferito
from catalog.models import Prodotto

# Create your views here.
def preferiti_toggle(request, pk):
    if not (request.user.is_authenticated and request.user.ruolo == 'acquirente'):
        messages.error(request, "Accedere come 'acquirente' per aggiungere un prodotto ai preferiti!")
        return redirect('catalogo')

    prodotto = get_object_or_404(Prodotto, pk=pk)
    if Preferito.objects.filter(acquirente=request.user, prodotto=prodotto).exists():
        Preferito.objects.filter(acquirente=request.user, prodotto=prodotto).delete()
        messages.success(request, "Prodotto rimosso dai preferiti.")
    else:
        Preferito.objects.create(acquirente=request.user, prodotto=prodotto)
        messages.success(request, "Prodotto aggiunto ai preferiti.")

    return redirect('dettagli_prodotto', pk=pk)

def preferiti_view(request):
    if not (request.user.is_authenticated and request.user.ruolo == 'acquirente'):
        return redirect('catalogo')
    
    lista_preferiti = Preferito.objects.filter(acquirente=request.user).order_by('-prodotto__disponibile','-data_aggiunta')
    
    return render(request, 'favorites/preferiti_template.html', {'preferiti': lista_preferiti})
    