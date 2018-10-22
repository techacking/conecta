from django.db import models
from home.models import *

# Create your models here.

class Entre(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    descricao = models.TextField()
    criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Agenda(models.Model):
    dataEntrada = models.DateField()
    dataSaida = models.DateField()
    status = models.IntegerField()

    pedido = models.ForeignKey(Pedido, null=True, blank=False, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.dataEntrada


class Consulta_Agenda(models.Model):
    dataconsultada = models.DateTimeField(auto_now_add=True)

    cliente = models.ForeignKey(Cliente, null=True, blank=False, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return [self.cliente, self.agenda, self.datarequisitada]
