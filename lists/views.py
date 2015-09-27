from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    ''' render takes the request as first parameter and
    name of the template to render.'''
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })
    # reference: look up dict.get
    # http://docs.python.org/3/library/stdtypes.html#dict.get
