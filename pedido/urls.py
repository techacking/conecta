from django.urls import path
from .views import *

urlpatterns = [

    path('pedido/', pedido, name='pedido'),
    path('pedido_novo/', pedido_novo, name='pedido_novo'),
    path('pedido_altera/<int:id>/', pedido_altera, name='pedido_altera'),
    path('pedido_deleta/<int:id>/', pedido_deleta, name='pedido_deleta'),

    path('orcamento/', orcamento, name='orcamento'),
    path('orcamento_novo/', orcamento_novo, name='orcamento_novo'),
    path('orcamento_altera/<int:id>/', orcamento_altera, name='orcamento_altera'),
    path('orcamento_deleta/<int:id>/', orcamento_deleta, name='orcamento_deleta'),
]