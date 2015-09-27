from django.test import TestCase

# Create your tests here.
class SmokeTest(TestCase):
    ''' Tests here will invoked by:
    python manage.py test
    '''    
    def test_bad_maths(self):
        ''' a deliberately failing test. '''
        self.assertEqual(1 + 1, 3)
