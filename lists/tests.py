from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page  # home_page in lists/view.py
from lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        ''' Check that resolve, when called with '/', the root
        of the site, finds a function called home_page. '''
        found = resolve('/')
        self.assertEqual(found.func, home_page) 

    def test_home_page_returns_correct_html(self):
        ''' Checks that we're render the correct template.'''
        request = HttpRequest()  # what django sees when browser asks for a page
        response = home_page(request)
        expected_html = render_to_string('home.html')
        # decode() converts response.content bytes into unicode;
        # allows us to compare strings with strings
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        ''' Checks that return HTML will have new item next to it,
        along with POST request.'''
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        # check that at least 1 Item saved to database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()  # same as objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(response.content.decode(), expected_html)

class ItemModelTest(TestCase):
    ''' new test model to create new records in database, and first
    unit test for using Django's Object-Relational Mapper (ORM). '''
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        # .objects is a class attribute of the database
        # .all() is a simple query to retrieve all records for table
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
        
