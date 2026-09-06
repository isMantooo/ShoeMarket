from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrazioneForm

# Create your views here.
def registrazione(request):
    if request.method == 'POST':
        form = RegistrazioneForm(request.POST)
        if form.is_valid(): 
            form.save() 
            messages.success(request, "Registrazione avvenuta con successo!")
            return redirect('catalogo')
    else:
        form = RegistrazioneForm()

    return render(request,'accounts/form_template.html', {'form' : form})
