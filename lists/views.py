from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
    ''' render takes the request as first parameter and
    name of the template to render.'''
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    return render(request, 'home.html')
        
    # reference: look up dict.get
    # http://docs.python.org/3/library/stdtypes.html#dict.get
