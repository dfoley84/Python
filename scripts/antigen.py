from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from webdriver_manager.chrome import ChromeDriverManager

Member = {
 1: {'Over16':'yes', 'FullName':'John Doe', 'DOB':'12/12/1990', 'Address':'Cork', 'City':'Cork', 'County':'Cork', 'Eircode':'P12', 'Phone': '085111111', 'email':'t@gmail.com'},
}


for k in Member:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.hse.ie/antigentesting/")
    driver.find_element_by_css_selector("input[type='radio'][value='Yes']").click()
    driver.find_element_by_xpath(".//*[@id='pT-Form-Submit-Btn']").click()

    if Member[k]["Over16"] == 'yes':
        driver.find_element_by_css_selector("input[type='radio'][value='16 and over']").click()
    else:
        driver.find_element_by_css_selector("input[type='radio'][value='under 16']").click()

    #FirstName     
    Name = Member[k]["FullName"].split(" ")
    FNAME = driver.find_element_by_id("id_first_name")
    FNAME.send_keys(Name[0])

    #SureName
    SNAME = driver.find_element_by_name("last_name")
    Surname = Member[k]["FullName"].split(" ")
    SNAME.send_keys(Name[1])

    #DOB
    DOB = driver.find_element_by_name("date_of_birth")
    DOB.send_keys(Member[k]["DOB"])

    #Address 
    Address1 = driver.find_element_by_name("address_line_1")
    Address1.send_keys(Member[k]["Address"])

    #City
    City = driver.find_element_by_name("city")
    City.send_keys(Member[k]["City"])

    #County
    County = Select(driver.find_element_by_name("county"))
    County.select_by_value(Member[k]["County"])

    #Eircode
    Eircode = driver.find_element_by_name("eircode")
    Eircode.send_keys(Member[k]["Eircode"])

    #Full Name
    FullName = driver.find_element_by_name("parent_name")
    FullName.send_keys(Member[k]["FullName"])

    #Phone
    Phone = driver.find_element_by_name("mobile")
    Phone.send_keys(Member[k]["Phone"])

    #Email
    Email = driver.find_element_by_name("email")
    Email.send_keys(Member[k]["email"])
 

    driver.find_element_by_css_selector("input[type='checkbox'][value='I agree']").click()
    driver.find_element_by_xpath(".//*[@id='pT-Form-Submit-Btn']").click()

