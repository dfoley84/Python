from logging import setLogRecordFactory
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



class GetLowBP(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)
   
    def test_lowbp(self):
        action = ActionChains(self.browser)
        self.browser.get("https://bloodpressure-ca-staging.azurewebsites.net")
        Systolic = self.browser.find_element_by_id("BP_Systolic")
        Systolic.clear()
        action.click(on_element = Systolic)
        action.send_keys(70)
        Diastolic = self.browser.find_element_by_id("BP_Diastolic")
        Diastolic.clear()
        action.click(on_element = Diastolic)
        action.send_keys(60)
        action.perform()
        SubmitButton = self.browser.find_element_by_xpath("//input[@value='Submit']")
        SubmitButton.submit()
        Message = self.browser.find_elements_by_tag_name("body")

        # To Do 
         ##Assert Not Working Correctly on the Unit Testing. 
        self.assertSetEqual("Low Blood Pressure", Message)
        
 
if __name__ == '__main__':
    unittest.main(verbosity=2)

