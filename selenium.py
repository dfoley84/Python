from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
  
# get geeksforgeeks.org
driver.get("")
  


# get element 
action = ActionChains(driver)
pageTitle = driver.title



element = driver.find_element_by_name("BP.Systolic")
element.clear()
action.click(on_element = element)
action.send_keys(150)

element1 = driver.find_element_by_name("BP.Diastolic")
element1.clear()
action.click(on_element = element1)
action.send_keys(60)
action.perform()

element2 = driver.find_element_by_xpath("//input[@value='Submit']")
element2.submit()



