from django.contrib import admin
from .models import *
# Register your models here.


class CondicaoAdmin(admin.ModelAdmin):
    list_display = ('condicao',)


class ServicoAdmin(admin.ModelAdmin):
    list_display = ('tiposervico',)

admin.site.register(TipoSala),
admin.site.register(Sala),
admin.site.register(Condicao, CondicaoAdmin),
admin.site.register(Cliente),
admin.site.register(Contato),
admin.site.register(Servicos, ServicoAdmin),