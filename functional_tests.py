from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # send special keys (ex. ENTER, CTRL modifiers)
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        ''' special method run before test. '''
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)  # selenium waits 3 sec. for something in page appear

    def tearDown(self):
        ''' special method run after test. '''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        ''' this is where main body of the test is. '''
        # Edith has heard about a cool new oneline to-do app.
        # She goes to check out its homepage.
        self.browser.get('http://localhost:8000')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in table"
        )

        # She enters "Use peacock feathers to make a fly" in another
        # text box inviting her to add another item
        self.fail('Finish the test!')
        

if __name__ == '__main__':
    unittest.main(warnings='ignore')  # supresses superfluous ResourceWarning
