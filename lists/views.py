from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    ''' render takes the request as first parameter and
    name of the template to render.'''
    return render(request, 'home.html')
