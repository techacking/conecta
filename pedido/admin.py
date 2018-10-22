from django.contrib import admin
from .models import *
# Register your models here.


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('status', 'cliente',)

class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('valor','pedido')

admin.site.register(Pedido, PedidoAdmin),
admin.site.register(Orcamento, OrcamentoAdmin),