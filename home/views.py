from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.views.generic.list import ListView

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def cliente_list(request):
    cliente = Cliente.objects.all()
    return render(request, 'cliente_list.html', {'cliente': cliente})

@login_required
def cliente_novo(request):
    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('cliente_list')
    return render(request, 'cliente_form.html', {'form': form})

@login_required
def cliente_altera(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    form = ClienteForm(request.POST or None, instance=cliente)

    if form.is_valid():
        form.save()
        return redirect('cliente_list')

    return render(request, 'cliente_form.html', {'form': form})

