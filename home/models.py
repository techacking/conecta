from django.db import models
from home.models import *


# Create your models here.

class TipoSala(models.Model):
    tipo = models.CharField(max_length=15)

    def __str__(self):
        return self.tipo


class Perfil(models.Model):
    perfil = models.CharField(max_length=50)

    def __str__(self):
        return self.pefil


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    login = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)

    perfil = models.ForeignKey(Perfil, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=40)
    cnpj = models.CharField(max_length=30)
    inscricaoestadual = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, blank=False)

    def __str__(self):
        return self.nome


class Condicao(models.Model):
    condicao = models.CharField(max_length=15)

    def __str__(self):
        return self.condicao


class Sala(models.Model):
    nome = models.CharField(max_length=30)
    capacidade = models.IntegerField()

    status = models.ForeignKey(Condicao, null=True, blank=True, on_delete=models.CASCADE)
    tipo = models.ManyToManyField(TipoSala)

    def __str__(self):
        return self.nome


class SalaDisponibilidade(models.Model):
    sala = models.ForeignKey(Sala, null=True, blank=True, on_delete=models.CASCADE)
    condicao = models.ForeignKey(Condicao, null=False, blank=False, on_delete=models.CASCADE)
    data_disponibilidade = models.DateField()

    def __str__(self):
        return self.sala


class Contato(models.Model):
    ddd = models.SmallIntegerField()
    telefone = models.IntegerField()
    tipo = models.CharField(max_length=20)

    cliente = models.ForeignKey(Cliente, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.ddd + self.telefone


class Endereco(models.Model):
    endereco = models.CharField(max_length=100)
    numero = models.IntegerField()
    cidade = models.CharField(max_length=80)
    estado = models.CharField(max_length=80)
    logradouro = models.CharField(max_length=20)
    cep = models.IntegerField()
    bairro = models.CharField(max_length=50)

    cliente = models.ForeignKey(Cliente, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.endereco


class MediaCliente(models.Model):
    site = models.CharField(max_length=40, null=True)
    foto = models.ImageField(upload_to='clients_photos', null=True, blank=True)

    cliente = models.ForeignKey(Cliente, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.site


class Servicos(models.Model):
    tiposervico = models.CharField(max_length=20)

    def __str__(self):
        return self.tiposervico


class Boleto(models.Model):
    vencimento = models.DateTimeField()
    valor = models.FloatField()
    taxa = models.FloatField()
    codigobarra = models.TextField()

    cliente = models.ForeignKey(Cliente, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.vencimento





class Boleto(models.Model):
    vencimento = models.DateTimeField()
    valor = models.FloatField()
    taxa = models.FloatField()
    codigobarra = models.TextField()

    cliente = models.ForeignKey(Cliente, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.vencimento


class Item(models.Model):
    nome = models.TextField()
    valor = models.FloatField()

    def __str__(self):
        return self.nome

from pedido.models import *

class Reserva(models.Model):
    entrada = models.DateTimeField()
    saida = models.DateTimeField()
    descricaoReserva = models.TextField()

    pedido = models.ForeignKey(Pedido, blank=True, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.entrada
class Evento(models.Model):
    titulo = models.TextField()
    tipo = models.TextField()

    item = models.ManyToManyField(Item)
    reserva = models.ForeignKey(Reserva, blank=False, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
class Arquivo(models.Model):
    caminho = models.TextField()
    titulo = models.CharField(max_length=30)
    formato = models.CharField(max_length=10)

    evento = models.ForeignKey(Evento, blank=None, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
