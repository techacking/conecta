from django.contrib import admin
from .models import *
# Register your models here.


class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'capacidade', 'status', 'tipo')

class TipoSalaAdmin(admin.ModelAdmin):
    list_display = ('tipo',)

class CondicaoAdmin(admin.ModelAdmin):
    list_display = ('condicao',)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'contato')

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone1', 'celular')

class ServicoAdmin(admin.ModelAdmin):
    list_display = ('tiposervico',)

class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'capacidade', 'status', 'tipo')

admin.site.register(TipoSala, TipoSalaAdmin),
admin.site.register(Sala, SalaAdmin),
admin.site.register(Condicao, CondicaoAdmin),
admin.site.register(Cliente, ClienteAdmin),
admin.site.register(Contato, ContatoAdmin),
admin.site.register(Servicos, ServicoAdmin),