from django.shortcuts import render


def index(request):
    return render(request, 'csite/index.html')