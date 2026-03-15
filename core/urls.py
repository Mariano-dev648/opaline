from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header  = '👑 Opaline — Painel Administrativo'
admin.site.site_title   = 'Opaline Admin'
admin.site.index_title  = 'Bem-vinda ao painel da Opaline'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('produtos.urls')),
    path('clientes/', include('clientes.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('pagamentos/', include('pagamentos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)