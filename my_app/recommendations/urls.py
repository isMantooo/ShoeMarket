from django.urls import path
from .views import consigliati_view

urlpatterns = [
    path('consigliati/', consigliati_view, name='consigliati'),
]

