from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import json
from faker import Faker

class UserFlowTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fake = Faker()
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def generate_random_user(self):
        name = self.fake.name()
        email = self.fake.email()
        password = self.fake.password(length=10)
        dob = self.fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y")
        hobby = random.choice(["Reading", "Gaming", "Cooking", "Hiking"])
        return {"name": name, "email": email, "password": password, "dob": dob, "hobby": hobby}

    def save_user_to_json(self, user_data, filename='test_users.json'):
        with open(filename, 'w') as file:
            json.dump(user_data, file)

    def load_user_from_json(self, filename='test_users.json'):
        with open(filename, 'r') as file:
            return json.load(file)

    def wait_and_click(self, by, identifier):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, identifier))).click()

    def wait_and_send_keys(self, by, identifier, keys):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, identifier))).clear()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, identifier))).send_keys(keys)

    def test_1_signup(self):
        user = self.generate_random_user()
        self.save_user_to_json(user)
        self.driver.get(f'{self.live_server_url}/signup')
        self.wait_and_send_keys(By.ID, 'name', user['name'])
        self.wait_and_send_keys(By.ID, 'email', user['email'])
        self.wait_and_send_keys(By.ID, 'password', user['password'])
        self.wait_and_click(By.XPATH, '//button[contains(text(), "Create Account")]')
        WebDriverWait(self.driver, 10).until(EC.url_contains('/profile'))
        self.assertIn('/', self.driver.current_url)

    def test_2_login(self):
        user = self.load_user_from_json()
        self.driver.get(f'{self.live_server_url}/login')
        self.wait_and_send_keys(By.ID, 'email', user['email'])
        self.wait_and_send_keys(By.ID, 'password', user['password'])
        self.wait_and_click(By.XPATH, '//button[contains(text(), "Login")]')
        WebDriverWait(self.driver, 10).until(EC.url_contains('/dashboard'))
        self.assertIn('/profile/', self.driver.current_url)

    def test_3_edit_profile(self):
        user = self.load_user_from_json()
        updated_user = self.generate_random_user()
        self.driver.get(f'{self.live_server_url}/profile?tab=edit')
        self.wait_and_send_keys(By.ID, 'name', updated_user['name'])
        self.wait_and_send_keys(By.ID, 'email', updated_user['email'])
        self.wait_and_send_keys(By.ID, 'password', updated_user['password'])
        self.wait_and_send_keys(By.ID, 'dob', updated_user['dob'])
        self.wait_and_send_keys(By.ID, 'new_hobby', updated_user['hobby'])
        self.wait_and_click(By.NAME, 'add_hobby')
        self.wait_and_click(By.XPATH, '//button[contains(text(), "Save")]')
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), updated_user['email']))
        self.save_user_to_json(updated_user)

    def test_4_filter_users_by_age(self):
        self.driver.get(f'{self.live_server_url}/main')
        self.wait_and_send_keys(By.ID, 'ageMin', '25')
        self.wait_and_send_keys(By.ID, 'ageMax', '30')
        self.wait_and_click(By.XPATH, '//button[contains(text(), "Filter")]')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'user-card')))
        users = self.driver.find_elements(By.CLASS_NAME, 'user-card')
        self.assertGreater(len(users), 0)

    def test_5_send_friend_request(self):
        self.driver.get(f'{self.live_server_url}/main')
        self.wait_and_click(By.XPATH, '//button[contains(@aria-label, "Add Friend")]')
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'friend-status'), 'Pending'))

    def test_6_accept_friend_request(self):
        sender = self.load_user_from_json()
        receiver = self.generate_random_user()
        self.save_user_to_json(receiver, 'receiver_user.json')
        
        # Sender sends friend request
        self.test_5_send_friend_request()
        
        # Log out sender
        self.driver.get(f'{self.live_server_url}/logout')
        
        # Log in as receiver
        self.driver.get(f'{self.live_server_url}/login')
        self.wait_and_send_keys(By.ID, 'email', receiver['email'])
        self.wait_and_send_keys(By.ID, 'password', receiver['password'])
        self.wait_and_click(By.XPATH, '//button[contains(text(), "Login")]')
        
        # Accept friend request
        self.driver.get(f'{self.live_server_url}/profile?tab=friends')
        self.wait_and_click(By.XPATH, '//button[contains(text(), "Accept")]')
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'friend-status'), 'Accepted'))
        self.assertGreater(len(friends), 0)
