from django.forms import ModelForm
from .models import *

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cnpj', 'inscricaoestadual', 'telefone',
                  'email', 'site', 'cep', 'endereco', 'numero', 'bairro',
                  'telefone', 'contato',
                  ]

class ContatoForm(ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'site',
                  'celular', 'telefone1', 'telefone2', 'foto'
                  ]