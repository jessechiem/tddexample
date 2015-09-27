from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from lists.views import home_page  # home_page in lists/view.py

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        ''' Check that resolve, when called with '/', the root
        of the site, finds a function called home_page. '''
        found = resolve('/')
        self.assertEqual(found.func, home_page) 

    def test_home_page_returns_correct_html(self):
        ''' Asserts that closing <html> tags & <title> appears
        in HttpResponse's contents. '''
        request = HttpRequest()  # what django sees when browser asks for a page
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do Lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
