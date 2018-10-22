from django.db import models
from home.models import *


class Pedido(models.Model):
    status = models.SmallIntegerField()
    datapedido = models.DateTimeField()
    dataagenda = models.DateTimeField()

    cliente = models.ForeignKey(Cliente, null=True, blank=False, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.status


class Pagamento(models.Model):
    datapagamento = models.DateTimeField()
    valor = models.FloatField()
    formaPagamento = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    cliente = models.ForeignKey(Cliente, blank=False, null=False, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, blank=False, null=False, on_delete=models.CASCADE)
    boleto = models.ForeignKey(Boleto, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.status


class Orcamento(models.Model):
    valor = models.FloatField()
    datageracao = models.DateTimeField()

    pedido = models.ForeignKey(Pedido, blank=False, null=False, on_delete=models.CASCADE)




