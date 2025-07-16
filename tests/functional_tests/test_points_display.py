from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestPointsDisplay:
    def test_points_display_disconnected(self):
        service = Service("tests/functional_tests/chromedriver.exe")
        self.browser = webdriver.Chrome(service=service)
        self.browser.get("http://localhost:5000/")
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[text()='Welcome to the GUDLFT Registration Portal!']"))
        )
        
        self.browser.find_element(By.LINK_TEXT, "View all club points").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, "points-table"))
        )
        
        assert self.browser.find_element(By.ID, "points-table").is_displayed()
        
        self.browser.close()
        
    def test_points_display_connected(self):
        service = Service("tests/functional_tests/chromedriver.exe")
        self.browser = webdriver.Chrome(service=service)
        self.browser.get("http://localhost:5000/")
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[text()='Welcome to the GUDLFT Registration Portal!']"))
        )
        
        self.browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
        self.browser.find_element(By.TAG_NAME, "button").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome')]"))
        )
        
        self.browser.find_element(By.LINK_TEXT, "View all club points").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, "points-table"))
        )
        
        assert self.browser.find_element(By.ID, "points-table").is_displayed()
        
        self.browser.close()