from django.forms import ModelForm
from .models import *

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['dataagenda','cliente','sala'
                  ]

class OrcamentoForm(ModelForm):
    class Meta:
        model = Orcamento
        fields = ['pedido','valor'
                  ]