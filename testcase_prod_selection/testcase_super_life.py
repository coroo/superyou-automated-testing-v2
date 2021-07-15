# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from decouple import config
import unittest, time, re

Email = config("EXISTING_USER_EMAIL", cast=str)
Password = config("EXISTING_USER_PASSWORD", cast=str)

class TestCaseLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge(config("DRIVER_PATH", cast=str))
        # self.driver = webdriver.Chrome(config("DRIVER_PATH", cast=str))
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_case_login(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("https://staging.superyou.co.id/") # Website Link

        # LOGIN PAGE #

        driver.find_element_by_id("masuk-button-header").click() # Login Button
        time.sleep(1)
        driver.find_element_by_id("user_email").click() # Email Field
        driver.find_element_by_id("user_email").send_keys(Email) # Email Field
        driver.find_element_by_id("user_password").click() # Password Field
        driver.find_element_by_id("user_password").send_keys(Password) # Password Field
        driver.find_element_by_id("login-button-loginpage").click() # Submit Button
        time.sleep(1)
        driver.find_element_by_id("superyou-logo-dashboard").click()


        driver.find_element_by_id("mulai-sekarang-homepage").click() # Mulai Sekarang Button at homepage
        driver.find_element_by_css_selector(".welcome-container button[type='submit']").click()

        time.sleep(5)

        nodes = []
        nodes = driver.find_elements_by_css_selector("#form-user #base-modal .form-product-selection .vs__selected-options input[class='vs__search']")
        nodes[0].click()
        driver.find_element_by_xpath("//div[@id='su-base-select']/div/ul/li[4]").click() # Click Super Life Protection

        nodes[1].click()
        driver.find_element_by_xpath("//div[@id='su-base-select']/div/ul/li[1]").click() # Click Bronze Plan

        time.sleep(2)

        assert "Kamu tidak dapat menambah produk lagi, uang pertanggungan yang didapat sudah mencapat batas 1.5 Milyar" in driver.page_source

        buttons = []
        buttons = driver.find_elements_by_css_selector("#form-user #product-selection .cta-buttons button")
        
        buttons[0].is_enabled() == False

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