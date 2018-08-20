from django.db import models

# Create your models here.

class TipoSala(models.Model):
    tipo = models.CharField(max_length=15)

    def __str__(self):
        return self.tipo

class Condicao(models.Model):
    condicao = models.CharField(max_length=15)

    def __str__(self):
        return self.condicao

class Sala(models.Model):
    nome = models.CharField(max_length=30)
    capacidade = models.IntegerField()
    status = models.ForeignKey(Condicao, null=True, blank=True, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoSala, null=True, blank=True, on_delete=models.CASCADE)

class Contato(models.Model):
    nome = models.CharField(max_length=35)
    email = models.EmailField(null=True)
    site = models.CharField(max_length=40, null=True)
    celular = models.IntegerField()
    telefone1 = models.IntegerField(null=True)
    telefone2 = models.IntegerField(null=True)
    foto = models.ImageField(null=True)

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=30)
    cnpj = models.IntegerField()
    inscricaoestadual = models.IntegerField()
    email = models.EmailField()
    site = models.CharField(max_length=50)
    cep = models.IntegerField()
    endereco = models.CharField(max_length=100)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=20)
    telefone = models.IntegerField()
    contato = models.ForeignKey(Contato, null=True, blank=True, on_delete=models.PROTECT)






