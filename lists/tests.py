from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page  # home_page in lists/view.py

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
