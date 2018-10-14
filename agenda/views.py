from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def agenda(request):
    entrada=Entre.objects.all()
    return render(request, 'agenda.html')