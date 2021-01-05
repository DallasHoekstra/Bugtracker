from django.shortcuts import render
from .models import Bug

def home(request):
    # values inside context will be available to the templates
    context = {
        'bugs': Bug.objects.all()
    }
    return render(request, 'bugtrackerApp/home.html', context)

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'bugtrackerApp/about.html', context)


