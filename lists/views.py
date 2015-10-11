from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.
def home_page(request):
    ''' render takes the request as first parameter and
    name of the template to render.'''
    # we can now remove the previous 'if request.method == 'POST''
    # code, since our new views will be doing that bulk of the work
    return render(request, 'home.html')
        
    # reference: look up dict.get
    # http://docs.python.org/3/library/stdtypes.html#dict.get

def view_list(request):
    ''' dummy view function for testing ListViewTest. '''
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/only-list-in-world/')
