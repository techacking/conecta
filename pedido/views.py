from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *

@login_required
def pedido(request):
    pedido = Pedido.objects.all()
    return render(request, 'pedido.html', {'pedido': pedido})

@login_required
def orcamento(request):
    orcamento = Orcamento.objects.all()
    return render(request, 'orcamento.html', {'orcamento': orcamento})

# ------------------------ Novo --------------------

@login_required
def pedido_novo(request):
    form = PedidoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('pedido')
    return render(request, 'pedido_form.html', {'form': form})

@login_required
def orcamento_novo(request):
    form = OrcamentoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('orcamento')
    return render(request, 'orcamento_form.html', {'form': form})


# ------------------------ Altera --------------------

@login_required
def pedido_altera(request, id):
    pedido = get_object_or_404(Pedido, pk=id)
    form = PedidoForm(request.POST or None, instance=pedido)

    if form.is_valid():
        form.save()
        return redirect('pedido')

    return render(request, 'pedido_form.html', {'form': form})

@login_required
def orcamento_altera(request, id):
    orcamento = get_object_or_404(Orcamento, pk=id)
    form = OrcamentoForm(request.POST or None, instance=orcamento)

    if form.is_valid():
        form.save()
        return redirect('pedido')

    return render(request, 'orcamento_form.html', {'form': form})

# ------------------------ Deleta --------------------


@login_required
def pedido_deleta(request, id):
    pedido = get_object_or_404(Pedido, pk=id)
    form = PedidoForm(request.POST or None, instance=pedido)

    if request.method == 'POST':
        pedido.delete()
        return redirect('pedido')

    return render(request, 'pedido_deleta.html', {'pedido': pedido})


@login_required
def orcamento_deleta(request, id):
    orcamento = get_object_or_404(Orcamento, pk=id)
    form = OrcamentoForm(request.POST or None, instance=orcamento)

    if request.method == 'POST':
        orcamento.delete()
        return redirect('orcamento')

    return render(request, 'orcamento_deleta.html', {'orcamento': orcamento})
