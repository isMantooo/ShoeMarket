from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RecensioneForm
from catalog.models import Prodotto
from .models import Recensione
# Create your views here.
def recensione_view(request, pk):
    if not (request.user.is_authenticated and request.user.ruolo == 'acquirente'):
        messages.error(request, "Accedi come 'acquirente' per poter recensire un prodotto!")
        return redirect('catalogo')

    prodotto = get_object_or_404(Prodotto, pk=pk)

    if Recensione.objects.filter(acquirente=request.user, prodotto=prodotto).exists():
        messages.error(request, "Non puoi aggiungere più recensioni allo stesso prodotto con lo stesso account.")
        return redirect('dettagli_prodotto', pk=pk)

    if request.method == 'POST':
        form = RecensioneForm(request.POST)
        if form.is_valid():
            recensione = form.save(commit=False)
            recensione.acquirente = request.user
            recensione.prodotto = prodotto
            recensione.save()
            messages.success(request, "Recensione aggiunta con successo!")
            return redirect('catalogo')
    else:
        form = RecensioneForm()

    return render(request, 'reviews/recensione_template.html', {'form': form})
