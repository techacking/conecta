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

]