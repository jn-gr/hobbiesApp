from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import json
from faker import Faker

class UserFlowTest(LiveServerTestCase):
    port = 8000
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fake = Faker()
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        cls.driver = webdriver.Chrome(options=options)
        cls.hobbies_pool = [
            "Reading", "Cooking", "Traveling", "Gaming", "Hiking",
            "Photography", "Painting", "Music", "Gardening", "Cycling"
        ]
        cls.generated_users = []

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def random_dob(self):
        return self.fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y")

    def generate_email(self, name):
        return name.lower().replace(" ", ".") + "@example.com"

    def signup_users(self):
        for _ in range(5):
            full_name = self.fake.name()
            email = self.generate_email(full_name)
            password = self.fake.password(length=10)
            dob = self.random_dob()
            hobbies = random.sample(self.hobbies_pool, k=random.randint(1, 5))
            user = {"full_name": full_name, "email": email, "password": password}
            self.generated_users.append(user)

            self.driver.get(f"{self.live_server_url}/")
            time.sleep(2)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "name"))).send_keys(full_name)
            self.driver.find_element(By.ID, "email").send_keys(email)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.ID, "dob").send_keys(dob)

            for hobby in hobbies:
                hobby_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Or type a new hobby']")
                hobby_input.clear()
                hobby_input.send_keys(hobby)
                self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div/div[2]/form/div[5]/div[3]/button").click()
                time.sleep(0.5)

            self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div/div[2]/form/button").click()
            time.sleep(2)
            self.driver.delete_all_cookies()

        with open("test_users.json", "w") as file:
            json.dump(self.generated_users, file, indent=4)

    def login(self, email, password):
        self.driver.get(f"{self.live_server_url}/login")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div/div[2]/form/button").click()
        time.sleep(2)

    def edit_profile(self, user):
        self.driver.get(f"{self.live_server_url}/profile")
        new_name = self.fake.name()
        new_email = self.generate_email(new_name)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "name"))).clear()
        self.driver.find_element(By.ID, "name").send_keys(new_name)
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys(new_email)
        user['full_name'] = new_name
        user['email'] = new_email
        time.sleep(2)
        self.driver.find_element(By.ID, "saveChanges").click()
        time.sleep(2)

    def test_user_flow(self):
        self.signup_users()
        for user in self.generated_users:
            self.login(user['email'], user['password'])
            self.edit_profile(user)
            self.driver.delete_all_cookies()
            time.sleep(2)