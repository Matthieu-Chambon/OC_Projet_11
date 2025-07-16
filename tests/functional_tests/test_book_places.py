from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from server import app

import time
import json
import shutil
import server
import threading


class TestBookPlaces:
    def setup_class(cls):
        """
        Load original data from JSON files before running tests.
        """
        with open('clubs.json', 'r') as f:
            clubs_data = json.load(f)
            clubs = clubs_data['clubs']
            cls.original_club = clubs[0]
            
        with open('competitions.json', 'r') as f:
            competitions_data = json.load(f)
            competitions = competitions_data['competitions']
            cls.original_competition = competitions[0]
    
    def setup_method(self):
        """
        Start the Flask server and create a backup of the clubs.json file before each test.
        """
        self.start_server()
        
        shutil.copyfile('clubs.json', 'clubs_backup.json')     
        server.clubs = server.loadClubs()
        
        self.authenticate()

    def teardown_method(self):
        """
        Stop the Flask server and restore the original clubs.json file after each test.
        """
        self.browser.close()
        
        shutil.move('clubs_backup.json', 'clubs.json')
        
    def start_server(self):
        """
        Start the Flask server in a separate thread.
        """
        self.server_thread = threading.Thread(target=app.run, kwargs={
            'port': 5001,
            'debug': False,
            'use_reloader': False
        })
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(1)
        
    def authenticate(self):
        """
        Authenticate the user by entering the email in the login form.
        """
        service = Service("tests/functional_tests/chromedriver.exe")
        self.browser = webdriver.Chrome(service=service)
        self.browser.get("http://127.0.0.1:5001/")
        
        self.browser.find_element(By.NAME, "email").send_keys(self.original_club['email'])
        self.browser.find_element(By.TAG_NAME, "button").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome')]"))
        )
        
    def test_book_places_success(self):
        """
        Test booking places successfully and check if points are deducted correctly.
        """
        self.browser.find_element(By.LINK_TEXT, "Book Places").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, "places-label"))
        )
        
        self.browser.find_element(By.ID, "places-label").send_keys("1")
        self.browser.find_element(By.TAG_NAME, "button").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome')]"))
        )
        
        assert self.browser.find_element(By.XPATH, "//li[contains(text(), 'Great-booking complete!')]")
        assert server.clubs[0]['points'] == str(int(self.original_club['points']) - 1)
        
        
    def test_book_places_insufficient_points(self):
        """
        Test booking places with insufficient points and check for error message.
        """
        self.browser.find_element(By.LINK_TEXT, "Book Places").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, "places-label"))
        )
        
        self.browser.find_element(By.ID, "places-label").send_keys("15")
        self.browser.find_element(By.TAG_NAME, "button").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//li[contains(text(), 'You do not have enough points to book this competition.')]"))
        )
        
        assert self.browser.find_element(By.XPATH, "//li[contains(text(), 'You do not have enough points to book this competition.')]")
        assert server.clubs[0]['points'] == self.original_club['points']
        
    def test_book_places_negative_number(self):
        """
        Test booking places with a negative number and check for error message.
        """
        self.browser.find_element(By.LINK_TEXT, "Book Places").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, "places-label"))
        )
        
        self.browser.find_element(By.ID, "places-label").send_keys("-1")
        self.browser.find_element(By.TAG_NAME, "button").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//li[contains(text(), 'You must book at least one place.')]"))
        )
        
        assert self.browser.find_element(By.XPATH, "//li[contains(text(), 'You must book at least one place.')]")
        assert server.clubs[0]['points'] == self.original_club['points']
        
    def test_book_more_than_12_places(self):
        """
        Test booking more than 12 places and check for error message.
        """
        self.browser.find_element(By.LINK_TEXT, "Book Places").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, "places-label"))
        )
        
        self.browser.find_element(By.ID, "places-label").send_keys("13")
        self.browser.find_element(By.TAG_NAME, "button").click()
        
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//li[contains(text(), 'You cannot book more than 12 places for a single competition.')]"))
        )
        
        assert self.browser.find_element(By.XPATH, "//li[contains(text(), 'You cannot book more than 12 places for a single competition.')]")
        assert server.clubs[0]['points'] == self.original_club['points']
        
        
        