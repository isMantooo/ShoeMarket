from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import registrazione

urlpatterns = [
    path('registrazione/', registrazione, name='registrazione'),
    path('login/', LoginView.as_view(template_name='accounts/login_template.html', next_page='catalogo'), name='login'),  
    path('logout/', LogoutView.as_view(next_page='catalogo'), name='logout'),
]