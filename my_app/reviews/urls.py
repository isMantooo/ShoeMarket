from django.urls import path
from .views import recensione_view

urlpatterns = [
    path('recensione/<int:pk>/', recensione_view, name='recensione'),
]
