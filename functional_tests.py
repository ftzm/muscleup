from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_start_list_and_retrieve_later(self):
        # open home page
        self.browser.get('http://localhost:8000')

        # title page shows correct name
        self.assertIn('MuscleUp', self.browser.title)
        self.fail('Finish test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
