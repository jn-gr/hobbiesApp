from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import json
from faker import Faker

class UserFlowTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fake = Faker()
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
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
        print("\n=== Starting User Signup Process ===")
        for i in range(5):
            print(f"\nCreating user {i+1}/5...")
            full_name = self.fake.name()
            email = self.generate_email(full_name)
            password = self.fake.password(length=10)
            dob = self.random_dob()
            hobbies = random.sample(self.hobbies_pool, k=random.randint(1, 5))
            user = {"full_name": full_name, "email": email, "password": password}
            self.generated_users.append(user)

            print(f"Name: {full_name}")
            print(f"Email: {email}")
            print(f"Date of Birth: {dob}")
            print(f"Selected Hobbies: {', '.join(hobbies)}")

            self.driver.get(f"{self.live_server_url}/signup")
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

            print("User successfully signed up!")

        print("\nSaving test users to test_users.json...")
        with open("test_users.json", "w") as file:
            json.dump(self.generated_users, file, indent=4)
        print("Test users saved successfully!")

    def login(self, email, password):
        print(f"\nAttempting login for user: {email}")
        self.driver.get(f"{self.live_server_url}/login")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div/div[2]/form/button").click()
        time.sleep(2)
        print("Login successful!")

    def edit_profile(self, user):
        print(f"\nEditing profile for user: {user['email']}")
        self.driver.get(f"{self.live_server_url}/profile")
        new_name = self.fake.name()
        new_email = self.generate_email(new_name)
        print(f"Updating name to: {new_name}")
        print(f"Updating email to: {new_email}")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "name"))).clear()
        self.driver.find_element(By.ID, "name").send_keys(new_name)
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys(new_email)
        user['full_name'] = new_name
        user['email'] = new_email
        time.sleep(2)
        self.driver.find_element(By.ID, "saveChanges").click()
        time.sleep(2)
        print("Profile updated successfully!")

    def test_user_flow(self):
        print("\n=== Starting User Flow Test ===")
        self.driver.get(f"{self.live_server_url}/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "app"))
        )
        print("Application loaded successfully")
        time.sleep(2)
        
        self.signup_users()
        print("\n=== Starting Login and Profile Edit Flow ===")
        for i, user in enumerate(self.generated_users, 1):
            print(f"\nTesting user {i}/{len(self.generated_users)}")
            self.login(user['email'], user['password'])
            self.edit_profile(user)
            self.driver.delete_all_cookies()
            time.sleep(2)
        print("\n=== User Flow Test Completed Successfully ===")