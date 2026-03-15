from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('minha-conta/', views.minha_conta, name='minha_conta'),
]