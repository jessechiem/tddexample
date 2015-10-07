from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # send special keys (ex. ENTER, CTRL modifiers)
import unittest

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        ''' special method run before test. '''
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)  # selenium waits 3 sec. for something in page appear

    def tearDown(self):
        ''' special method run after test. '''
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        ''' Begin to refactor better by using an inline, helper function;
        remember that only methods that begin with test_ will get run as tests.'''
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        ''' this is where main body of the test is. '''
        # Edith has heard about a cool new oneline to-do app.
        # She goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices page title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peaccock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')  # checks if string matches a regex
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Now a new user, Francis, comes along to the site.
    
        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Buy milk', page_text)
       
        # Satisfied, they both go back to sleep 

        # She visits that URL - her to-do list is still there.

#if __name__ == '__main__':
#    unittest.main(warnings='ignore')  # supresses superfluous ResourceWarning

# now we can run with: python manage.py test functional_tests
