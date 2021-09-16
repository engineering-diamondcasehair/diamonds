import unittest
from selenium import webdriver

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()


    def tearDown(self):
        self.driver.quit()

class UITest(BaseTest):

    def test_homepage(self):
        self.driver.get("http://127.0.0.1:5000/")

        # Test Title
        title = self.driver.find_element_by_tag_name("h1")
        self.assertEquals(u'Welcome To Diamond Case Beauty Supply', 
            title.text)
        self.assertEquals(u'rgba(255, 255, 255, 1)', title.value_of_css_property("color"))
        self.assertEquals(['display-1'], title.get_attribute('class').split())
        
        
        # Test SubTitle
        subtitle = self.driver.find_element_by_tag_name("h2")
        self.assertEquals(u'Where Beauty Meets Convenience.', 
            subtitle.text)
        self.assertEquals(u'rgba(255, 255, 255, 1)', subtitle.value_of_css_property("color"))
        self.assertEquals(['display-4'], subtitle.get_attribute('class').split())

if __name__ == '__main__':
    unittest.main()