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
def contato_list(request):
    contato = Contato.objects.all()
    return render(request, 'contato_list.html', {'contato': contato})

# ----------------- Novo ---------------------------------

@login_required
def cliente_novo(request):
    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('cliente_list')
    return render(request, 'cliente_form.html', {'form': form})

@login_required
def contato_novo(request):
    form = ContatoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('contato_list')
    return render(request, 'contato_form.html', {'form': form})

# ----------------- Altera ---------------------------------


@login_required
def cliente_altera(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    form = ClienteForm(request.POST or None, instance=cliente)

    if form.is_valid():
        form.save()
        return redirect('cliente_list')

    return render(request, 'cliente_form.html', {'form': form})

@login_required
def contato_altera(request, id):
    contato = get_object_or_404(Contato, pk=id)
    form = ContatoForm(request.POST or None, request.FILES or None, instance=contato)

    if form.is_valid():
        form.save()
        return redirect('contato_list')

    return render(request, 'contato_form.html', {'form': form})


# ----------------- Deleta ---------------------------------

@login_required
def contato_deleta(request, id):
    contato = get_object_or_404(Contato, pk=id)
    form = ContatoForm(request.POST or None, request.FILES or None, instance=contato)

    if request.method == 'POST':
        form.delete()
        return redirect('contato_list')

    return render(request, 'contato_deleta.html', {'contato': contato})

