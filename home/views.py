from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from django.views.generic.list import ListView
from .models import Cliente


@login_required
def home(request):
    return render(request, 'home.html')


# CBV ------------ ListView ---------------

class Lista(ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'

# CBV -------------------------------------



@login_required
def contato_list(request):
    contato = Contato.objects.all()
    return render(request, 'contato_list.html', {'contato': contato})

@login_required
def sala_list(request):
    sala = Sala.objects.all()
    return render(request, 'sala_list.html', {'sala': sala})



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

@login_required
def sala_novo(request):
    form = SalaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('sala_list')
    return render(request, 'sala_form.html', {'form': form})



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

@login_required
def sala_altera(request, id):
    sala = get_object_or_404(Sala, pk=id)
    form = SalaForm(request.POST or None, instance=sala)

    if form.is_valid():
        form.save()
        return redirect('sala_list')

    return render(request, 'sala_form.html', {'form': form})


# ----------------- Deleta ---------------------------------

@login_required
def cliente_deleta(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    form = ClienteForm(request.POST or None, instance=cliente)

    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_list')

    return render(request, 'cliente_deleta.html', {'cliente': cliente})


@login_required
def contato_deleta(request, id):
    contato = get_object_or_404(Contato, pk=id)
    form = ContatoForm(request.POST or None, request.FILES or None, instance=contato)

    if request.method == 'POST':
        contato.delete()
        return redirect('contato_list')

    return render(request, 'contato_deleta.html', {'contato': contato})

@login_required
def sala_deleta(request, id):
    sala = get_object_or_404(Sala, pk=id)
    form = SalaForm(request.POST or None, instance=sala)

    if request.method == 'POST':
        sala.delete()
        return redirect('sala_list')

    return render(request, 'sala_deleta.html', {'sala': sala})
