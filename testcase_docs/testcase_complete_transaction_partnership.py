# Last tested 3/11/2021 14:21

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from decouple import config
import unittest, time, re

# Account Data
PaymentMethod = config("PAYMENT_METHOD", cast=str)
URL = config("TRANSACTION_REDIRECTED_TO_LINK", cast=str)

CardName = config("CARD_NAME", cast=str)
CardNum = config("CARD_NUM", cast=str)
CardCVC = config("CARD_CVC", cast=str)
 
class TestCaseSingleProduct(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge(config("DRIVER_PATH", cast=str))
        # self.driver = webdriver.Chrome(config("DRIVER_PATH", cast=str))
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_case_NewUser_SingleProduct(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(URL) # Website Link
        time.sleep(1) # In Second

        # driver.find_element_by_xpath("//div[@id='su-base-select']/div/div/div").click()
        # driver.find_element_by_xpath("//div[@id='su-base-select']/div/ul/li[3]").click()
        # driver.find_element_by_xpath("//div[@id='underwriting']/div/div/div/div[2]/div/button").click()
        # driver.find_element_by_id("yesno-1").click()
        # driver.find_element_by_xpath("//div[@id='underwriting']/div/div/div/div[2]/div/button").click()
        # driver.find_element_by_xpath("//div[@id='underwriting']/div/div/div/div[2]/div/button/span").click()

        # Halaman pembayaran
        time.sleep(1)
        driver.find_element_by_xpath("//section[@id='sovia-payment']/form/div/div[2]/div[2]/div[2]/div/label").click() # Click S&K 1
        time.sleep(1)
        driver.find_element_by_xpath("//section[@id='sovia-payment']/form/div/div[2]/div[2]/div[3]/div/label").click() # Click S&K 2
        time.sleep(1)
        driver.find_element_by_xpath("//section[@id='sovia-payment']/form/div/div[2]/div[2]/div[4]/div/label").click() # Click S&K 3
        time.sleep(1)

        if (PaymentMethod) == 'faspay':
            # Pilih metode pembayaran
            driver.find_element_by_id("next-step").click() # SUBMIT

            # Halaman Faspay
            driver.find_element_by_name("CARDNAME").click()
            driver.find_element_by_name("CARDNAME").send_keys(CardName) # Input Card Name
            driver.find_element_by_name("CARDTYPE").click()
            driver.find_element_by_id("CARDNOSHOWFORMAT").click()
            driver.find_element_by_id("CARDNOSHOWFORMAT").send_keys(CardNum) # Input Card Number
            driver.find_element_by_name("CARDCVC").click()
            driver.find_element_by_name("CARDCVC").send_keys(CardCVC) # Input CVC
            driver.find_element_by_id("month").click()
            Select(driver.find_element_by_id("month")).select_by_visible_text("May")
            driver.find_element_by_id("month").click()
            driver.find_element_by_id("year").click()
            Select(driver.find_element_by_id("year")).select_by_visible_text("2021")
            driver.find_element_by_id("year").click()
            driver.find_element_by_name("submit").click() # Click Submit button
            time.sleep(2)
            driver.find_element_by_link_text("LIHAT AKUN KAMU").click()
            time.sleep(6)
        
        elif (PaymentMethod) == 'mandiri':
            # Pilih metode pembayaran
            mandiri = driver.find_element_by_xpath("/html/body/section/form/div/div[2]/div[2]/div[8]/div/div/div/div[1]/div/div[2]/a/div")
            mandiri.click()
            driver.find_element_by_id("next-step").click() # SUBMIT

        elif (PaymentMethod) == 'permata':
            # Pilih metode pembayaran
            permata = driver.find_element_by_xpath("/html/body/section/form/div/div[2]/div[2]/div[8]/div/div/div/div[1]/div/div[3]/a/div")
            permata.click()
            driver.find_element_by_id("next-step").click() # SUBMIT

        elif (PaymentMethod) == 'indomaret':
            # Pilih metode pembayaran
            indomaret = driver.find_element_by_xpath("/html/body/section/form/div/div[2]/div[2]/div[8]/div/div/div/div[1]/div/div[4]/a/div")
            indomaret.click()
            driver.find_element_by_id("next-step").click() # SUBMIT

        elif (PaymentMethod) == 'gopay':
            # Pilih metode pembayaran
            gopay = driver.find_element_by_xpath("/html/body/section/form/div/div[2]/div[2]/div[8]/div/div/div/div[1]/div/div[5]/a/div")
            gopay.click()
            driver.find_element_by_id("next-step").click() # SUBMIT

        else:
            print("Wrong Input. Please input 'faspay', 'mandiri', 'permata', 'indomaret' or 'gopay' in lower case letters.")

        time.sleep(30)
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