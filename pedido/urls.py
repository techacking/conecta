from django.urls import path
from .views import *

urlpatterns = [

    path('pedido/', pedido, name='pedido'),
    path('pedido_novo/', pedido_novo, name='pedido_novo'),
    path('pedido_altera/<int:id>/', pedido_altera, name='pedido_altera'),

]