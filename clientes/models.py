from django.db import models
from django.contrib.auth.models import AbstractUser
import re


class Cliente(AbstractUser):
    # Dados pessoais
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    # Preferências
    aceita_newsletter = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'


class Endereco(models.Model):
    TIPOS = [
        ('entrega', 'Entrega'),
        ('cobranca', 'Cobrança'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='enderecos')
    tipo = models.CharField(max_length=10, choices=TIPOS, default='entrega')
    nome_destinatario = models.CharField(max_length=200)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    principal = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return f'{self.logradouro}, {self.numero} — {self.cidade}/{self.estado}'