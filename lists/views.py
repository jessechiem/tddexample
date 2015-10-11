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

def view_list(request, list_id):
    ''' dummy view function for testing ListViewTest. '''
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
