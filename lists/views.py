from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    ''' render takes the request as first parameter and
    name of the template to render.'''
    # dummy return value for POST test before we actually
    # pass the POST parameter to the template
    if request.method == 'POST':
        return HttpResponse(request.POST['item_text'])
    return render(request, 'home.html')
