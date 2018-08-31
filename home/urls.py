from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [

    path('home/', home, name='home'),

    path('cliente/', cliente_list, name='cliente_list'),
    path('cliente_novo/', cliente_novo, name='cliente_novo'),
    path('cliente_altera/<int:id>/', cliente_altera, name='cliente_altera'),
    path('cliente_deleta/<int:id>/', cliente_deleta, name='cliente_deleta'),

    path('contato/', contato_list, name='contato_list'),
    path('contato_novo/', contato_novo, name='contato_novo'),
    path('contato_altera/<int:id>/', contato_altera, name='contato_altera'),
    path('contato_deleta/<int:id>/', contato_deleta, name='contato_deleta'),

    path('sala/', sala_list, name='sala_list'),
    path('sala_novo/', sala_novo, name='sala_novo'),
    path('sala_altera/<int:id>/', sala_altera, name='sala_altera'),
    path('sala_deleta/<int:id>/', sala_deleta, name='sala_deleta'),
]