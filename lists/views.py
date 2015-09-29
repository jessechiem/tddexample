from django.shortcuts import render
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
    ''' render takes the request as first parameter and
    name of the template to render.'''
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        # objects.create is shorthand for creating
        # new Item without calling .save()
        Item.objects.create(text=new_item_text)
    else:
        new_item_text = ''

    return render(request, 'home.html', {
        'new_item_text': new_item_text,
    })
    # reference: look up dict.get
    # http://docs.python.org/3/library/stdtypes.html#dict.get
