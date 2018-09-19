from django.db import models
from home.models import *
import random

def codigo():
    codi = ''
    for i in range(0, 5):
        codi += random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    while Orcamento.objects.filter(cod=codi):
        codi = codigo()
    return codi

class Pedido(models.Model):
    status = models.CharField(max_length=15)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)

class Orcamento(models.Model):
    cod = models.CharField(max_length=5, default=codigo, unique=True)
    dataini = models.DateTimeField()
    dataterm = models.DateTimeField()
    contato = models.ForeignKey(Contato, null=True, blank=True, on_delete=models.PROTECT)
    sala = models.ForeignKey(Sala, null=True, blank=True, on_delete=models.PROTECT)
    servicos = models.ForeignKey(Servicos, null=True, blank=True, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=5, decimal_places=2, null=True)



