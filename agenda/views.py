from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
import json

@login_required
def agenda(request):
    eventos = Orcamento.objects.all()
	eventosList = []
	for evento in eventos:
		eventoDict = {
			"title": str(evento.contato),
			"startdate": str(evento.dataini),
			"enddate": str(evento.dataterm),
		}
		eventosList.append(eventoDict)
    return render(request, 'agenda.html', {'eventosList': json.dumps(eventosList)})