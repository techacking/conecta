from django.forms import ModelForm
from .models import *

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['status', 'cliente',
                  ]

class OrcamentoForm(ModelForm):
    class Meta:
        model = Orcamento
        fields = ['cod', 'dataini', 'dataterm', 'contato', 'sala', 'servicos', 'valor',
                  ]