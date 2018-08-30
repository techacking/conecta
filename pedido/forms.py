from django.forms import ModelForm
from .models import *

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['status','cliente',]