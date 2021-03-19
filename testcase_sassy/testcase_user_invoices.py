# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from decouple import config
import unittest, time, re

Email = config("SASSY_EMAIL", cast=str)
Password = config("SASSY_PASSWORD", cast=str)
Filename = "test"

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge(config("DRIVER_PATH", cast=str))
        # self.driver = webdriver.Chrome(config("DRIVER_PATH", cast=str))
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("https://staging.superyou.co.id/sassy/login") # Website Link

        # Login
        driver.find_element_by_xpath("/html/body/div/div/form/div[1]/input").click() # Email field
        driver.find_element_by_xpath("/html/body/div/div/form/div[1]/input").clear()
        driver.find_element_by_xpath("/html/body/div/div/form/div[1]/input").send_keys(Email) # Input email
        driver.find_element_by_xpath("/html/body/div/div/form/div[2]/input").clear()
        driver.find_element_by_xpath("/html/body/div/div/form/div[2]/input").send_keys(Password) # Input password
        
        driver.find_element_by_xpath("//button[@type='submit']").click() # Login button
        time.sleep(2)

        driver.find_element_by_xpath("//div[@id='nova']/div/div/h3[2]/span").click() # Resources
        driver.find_element_by_xpath("//div[@id='nova']/div/div/h4[10]").click() # Policies
        driver.find_element_by_link_text("User Invoices").click() # User Invoices
        time.sleep(300)

        driver.close()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
