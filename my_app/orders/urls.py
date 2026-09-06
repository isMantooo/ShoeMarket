from django.urls import path
from .views import ordine_view, storico_ordini

urlpatterns = [
    path('acquisto/<int:pk>/', ordine_view, name='acquisto'),
    path('storico_ordini/', storico_ordini, name='storico_ordini'),
]