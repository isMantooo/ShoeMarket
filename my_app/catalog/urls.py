from django.urls import path
from .views import catalogo_view, crea_prodotto, dettagli_prodotto, venditore_view, rimuovi_prodotto

urlpatterns = [
    path('catalogo/', catalogo_view, name='catalogo'),
    path('nuovo_prodotto/', crea_prodotto, name='nuovo_prodotto'),
    path('prodotto/<int:pk>/', dettagli_prodotto ,name='dettagli_prodotto'),
    path('venditore/', venditore_view, name='venditore'),
    path('rimuovi_prodotto/<int:pk>/', rimuovi_prodotto, name='rimuovi_prodotto'),
]
