from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page  # home_page in lists/view.py
from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):
    ''' From TDD p 77: When we run unit tests (NOT functional tests),
    Django test runner automatically creates a brand new test database
    (separate from the real one), which it can safely reset before each
    individual test is run, and then throw away at the end. But our
    functional tests currently run against the 'real' database, db.sqlite3 '''
    
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


class ListAndItemModelsTest(TestCase):
    ''' new test model to create new records in database, and first
    unit test for using Django's Object-Relational Mapper (ORM). '''
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        # .objects is a class attribute of the database
        # .all() is a simple query to retrieve all records for table
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
        

class ListViewTest(TestCase):
    ''' Django Test Client for testing views, templates, and URLs
    working together; i.e checking URL resolution explicitly, view
    functions, and views rendering templates correctly. '''
    def test_uses_list_template(self):
        ''' Check to see if view is using the different template,
        after view_list in views.py is updated with list.html '''
        response = self.client.get('/lists/only-list-in-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        # instead of calling view function directly, we
        # use Django test client (.client part of TestCase)
        response = self.client.get('/lists/only-list-in-world/')

        # assertContains, as opposed to assertEquals, can deal
        # with rasponses and bytes of their content.
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):
    ''' Test class for new list creation. '''

    def test_saving_a_POST_request(self):
        ''' Checks that return HTML will have new item next to it,
        along with POST request. Always redirect after a post. '''
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        # check that at least 1 Item saved to database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()  # same as objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        ''' separate unit test for checking redirect post. '''
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        # instead of assertEquals, we'll use another of Django test
        # client's helper functions instead
        self.assertRedirects(response, '/lists/only-list-in-world/')
