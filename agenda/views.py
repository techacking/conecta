from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
import json

@login_required
def agenda(request):
    eventos = Entre.objects.all()
    eventos_list = []
    for evento in eventos:
        evento_dict = {
            "title": str(evento.name),
            "startdate": str(evento.date),
            "enddate": str(evento.date),
            "id": str(evento.id),
        }
        eventos_list.append(evento_dict)
    return render(request, 'agenda.html', {'eventosList': json.dumps(eventos_list)})