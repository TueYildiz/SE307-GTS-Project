from django.shortcuts import render
from .models import Thesis

def thesis_list(request):
    theses = Thesis.objects.all()
    context = {
        'theses': theses
    }
    return render(request, 'thesis_list.html', context)