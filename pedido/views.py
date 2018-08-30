from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *

@login_required
def pedido(request):
    pedido = Pedido.objects.all()
    return render(request, 'pedido.html', {'pedido': pedido})

# ------------------------ Novo --------------------

@login_required
def pedido_novo(request):
    form = PedidoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('pedido')
    return render(request, 'pedido_form.html', {'form': form})


# ------------------------ Altera --------------------

@login_required
def pedido_altera(request, id):
    pedido = get_object_or_404(Pedido, pk=id)
    form = PedidoForm(request.POST or None, instance=pedido)

    if form.is_valid():
        form.save()
        return redirect('pedido')

    return render(request, 'pedido_form.html', {'form': form})

# ------------------------ Deleta --------------------
