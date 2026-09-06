from django.urls import path
from .views import preferiti_toggle, preferiti_view

urlpatterns = [
    path('preferiti_toggle/<int:pk>/', preferiti_toggle, name='preferiti_toggle'),
    path('preferiti/', preferiti_view, name='preferiti'),
]