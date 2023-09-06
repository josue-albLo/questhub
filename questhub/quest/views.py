from django.shortcuts import render

# Create your views here.

def index(response):
    context = {'name': 'questhub'}
    return render(response, "quest/index.html", context)