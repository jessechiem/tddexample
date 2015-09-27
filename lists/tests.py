from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page  # home_page in lists/view.py

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        ''' Check that resolve, when called with '/', the root
        of the site, finds a function called home_page. '''
        found = resolve('/')
        self.assertEqual(found.func, home_page) 
