from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cliente, Endereco


class EnderecoInline(admin.TabularInline):
    model = Endereco
    extra = 1


@admin.register(Cliente)
class ClienteAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'cpf', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'cpf']
    inlines = [EnderecoInline]
    fieldsets = UserAdmin.fieldsets + (
        ('Dados Opaline', {'fields': ('cpf', 'telefone', 'data_nascimento', 'aceita_newsletter')}),
    )