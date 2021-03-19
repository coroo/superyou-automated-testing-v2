# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from decouple import config
import unittest, time, re

Username = config("DOCS_USERNAME", cast=str)
Password = config("DOCS_PASSWORD", cast=str)
UserID = config("DOCS_USER_ID", cast=str)

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
        driver.get("https://staging-partnership.superyou.co.id/dev/docs#/") # Website Link
        time.sleep(1)

        # Login
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/section/div/button").click() # Click Authroize Button
        driver.find_element_by_id("oauth_username").click() # Click username field
        driver.find_element_by_id("oauth_username").clear()
        driver.find_element_by_id("oauth_username").send_keys(Username) # Enter username
        driver.find_element_by_id("oauth_password").clear()
        driver.find_element_by_id("oauth_password").send_keys(Password) # Enter password
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[4]/button[1]").click() # Click authorize button
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/section/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[3]/button[2]").click() # Click close button
        time.sleep(2)

        # Create New Transaction
        driver.find_element_by_xpath("//div[@id='operations-transactions-create_transaction_for_user_api_v1_transactions_create__user_id__post']/div/div").click() # POST create new transaction
        driver.find_element_by_xpath("//div[@id='operations-transactions-create_transaction_for_user_api_v1_transactions_create__user_id__post']/div[2]/div/div[2]/div/div[2]/button").click() # Try it out button
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[4]/section/div/span[4]/div/div/div/span[1]/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/input").click() # user_id field
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[4]/section/div/span[4]/div/div/div/span[1]/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/input").clear()
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[4]/section/div/span[4]/div/div/div/span[1]/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/input").send_keys(UserID) # Input user_id
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[4]/section/div/span[4]/div/div/div/span[1]/div/div[2]/div/div[2]/div[3]/div[2]/div/div/div/textarea").click() # Request JSON body field
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[4]/section/div/span[4]/div/div/div/span[1]/div/div[2]/div/div[2]/div[3]/div[2]/div/div/div/textarea").clear()
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div[4]/section/div/span[4]/div/div/div/span[1]/div/div[2]/div/div[2]/div[3]/div[2]/div/div/div/textarea").send_keys("""{
  "product_slug": "super-care-protection",
  "product_code": "DSCPR11",
  "product_plan_code": "silver-plan-tanpa-perlindungan-covid-19",
  "holder_name": "Richard",
  "holder_gender": "MALE",
  "holder_dob": "21/06/1998",
  "holder_email": "abcsy_newuser00033@email.com",
  "holder_mobile_number": "081297648974",
  "insured_for": "SELF",
  "insured_name": "Mama",
  "insured_dob": "12/06/1998",
  "channel": "partnership",
  "rider_codes": "",
  "is_assist": true
}""") # Input request JSON body
        driver.find_element_by_xpath("//div[@id='operations-transactions-create_transaction_for_user_api_v1_transactions_create__user_id__post']/div[2]/div/div[3]/button").click() # Press execute button
        time.sleep(240)

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
