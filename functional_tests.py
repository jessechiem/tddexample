from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        ''' special method run before test. '''
        self.browser = webdriver.Firefox()
        self.browser.implicity_wait(3)  # selenium waits 3 sec. for something in page appear

    def tearDown(self):
        ''' special method run after test. '''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        ''' this is where main body of the test is. '''
        # Edith has heard about a cool new oneline to-do app.
        # She goes to check out its homepage.
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')  # produces fail message provided

        # She is invited to enter a to-do item straight away
        # [ ... other comments to follow ...]

if __name__ == '__main__':
    unittest.main(warnings='ignore')  # supresses superfluous ResourceWarning
