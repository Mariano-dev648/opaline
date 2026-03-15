from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('pix/<uuid:codigo>/', views.pagar_pix, name='pagar_pix'),
    path('webhook/', views.webhook_mp, name='webhook'),
    path('sucesso/<uuid:codigo>/', views.sucesso, name='sucesso'),
]