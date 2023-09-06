from django.shortcuts import render

# Create your views here.

def index(response):
    context = {'name': 'questhub'}
    return render(response, "quest/index.html", context)

def mian_page(response):
    return render(response, 'quest/main.html')

def answer(response):
    return render(response, 'quest/answers.html')