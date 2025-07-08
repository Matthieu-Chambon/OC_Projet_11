from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class TestAuthentication:
    def test_authenticate_with_valid_email(self):
        service = Service("tests/functional_tests/chromedriver.exe")
        self.browser = webdriver.Chrome(service=service)
        self.browser.get("http://127.0.0.1:5000/")
        
        self.browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
        self.browser.find_element(By.TAG_NAME, "button").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h2"))
        )
        
        assert self.browser.find_element(By.TAG_NAME, "h2").text == "Welcome, john@simplylift.co"
        
        self.browser.close()
        
    def test_authenticate_with_invalid_email(self):
        service = Service("tests/functional_tests/chromedriver.exe")
        self.browser = webdriver.Chrome(service=service)
        self.browser.get("http://127.0.0.1:5000/")
        
        self.browser.find_element(By.NAME, "email").send_keys("invalid@email.com")
        self.browser.find_element(By.TAG_NAME, "button").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.TAG_NAME, "li"))
        )
        
        assert self.browser.find_element(By.TAG_NAME, "li").text == "Adresse email inconnue, veuillez réessayer."
        
        self.browser.close()