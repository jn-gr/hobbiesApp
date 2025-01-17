from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
from faker import Faker

class UserFlowTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = "127.0.0.1"
        cls.port = 8000
        super().setUpClass()
        cls.fake = Faker()
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        # options.add_argument('--headless')
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
        for i in range(2):
            print(f"\nCreating user {i+1}/2...")
            full_name = self.fake.name()
            email = self.generate_email(full_name)
            password = self.fake.password(length=10)
            dob = self.random_dob()
            hobbies = random.sample(self.hobbies_pool, k=random.randint(1, 5))
            user = {"full_name": full_name, "email": email, "password": password}
            self.generated_users.append(user)

            self.driver.get(f"{self.live_server_url}")
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="app"]/div/header/div/div/a').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div[2]/form/p/a').click()
            time.sleep(2)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "name"))).send_keys(full_name)
            time.sleep(1)
            self.driver.find_element(By.ID, "email").send_keys(email)
            time.sleep(1)
            self.driver.find_element(By.ID, "password").send_keys(password)
            time.sleep(1)
            self.driver.find_element(By.ID, "dob").send_keys(dob)
            time.sleep(1)

            for hobby in hobbies:
                hobby_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Or type a new hobby']")
                hobby_input.clear()
                time.sleep(0.5)
                hobby_input.send_keys(hobby)
                time.sleep(0.5)
                self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div/div[2]/form/div[5]/div[3]/button").click()
                time.sleep(1)

            self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div/div[2]/form/button").click()
            time.sleep(3)
            self.driver.delete_all_cookies()
            time.sleep(2)

    def login(self, email, password):
        self.driver.get(f"{self.live_server_url}")
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="app"]/div/header/div/div/a').click()
        time.sleep(2)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        time.sleep(1)
        self.driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div/div[2]/form/button").click()
        time.sleep(3)

    def edit_profile(self, user):
        new_name = self.fake.name()
        new_email = self.generate_email(new_name)
        new_dob = self.random_dob()
        new_password = self.fake.password(length=10)

        # Edit Name
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "name"))).clear()
        time.sleep(1)
        self.driver.find_element(By.ID, "name").send_keys(new_name)
        time.sleep(1)

        # Edit Email
        self.driver.find_element(By.ID, "email").clear()
        time.sleep(1)
        self.driver.find_element(By.ID, "email").send_keys(new_email)
        time.sleep(1)

        # Edit Date of Birth
        self.driver.find_element(By.ID, "dob").clear()
        time.sleep(1)
        self.driver.find_element(By.ID, "dob").send_keys(new_dob)
        time.sleep(1)

        # Save Changes
        self.driver.find_element(By.ID, "saveChanges").click()
        time.sleep(3)

        # Remove one hobby
        remove_hobby_buttons = self.driver.find_elements(By.ID, "removeHobby")
        if remove_hobby_buttons:
            remove_hobby_buttons[0].click()
            time.sleep(1)

        # Add a new hobby
        self.driver.find_element(By.XPATH, '//*[@id="editHobby"]').click()
        time.sleep(2)
        hobby_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/input"))
        )
        new_hobby = random.choice(self.hobbies_pool)
        hobby_input.send_keys(new_hobby)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/button").click()
        time.sleep(2)

        self.driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/button").click()

        # Save Changes
        self.driver.find_element(By.ID, "saveChanges").click()
        time.sleep(3)

        # Navigate to Security Tab
        self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div/div[1]/div/nav/button[2]").click()
        time.sleep(2)

        # Change Password
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='oldPassword']"))).send_keys(user['password'])
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//*[@id='newPassword']").send_keys(new_password)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//*[@id='confirmPassword']").send_keys(new_password)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div/div[1]/div/nav/button[2]").click()
        time.sleep(3)

        # Update user dictionary
        user['full_name'] = new_name
        user['email'] = new_email
        user['dob'] = new_dob
        user['password'] = new_password

    def age_filtering(self):
        self.driver.get(f"{self.live_server_url}")
        time.sleep(2)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/main/div/div[1]/div[2]/div/div/input[1]"))).clear()
        self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div[1]/div[2]/div/div/input[1]").send_keys(18)
        self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div[1]/div[2]/div/div/input[2]").send_keys(60)
        self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div[1]/div[2]/button").click()
        time.sleep(5)

    def send_friend_requests(self):
        print("\n=== Sending Friend Requests ===")
        time.sleep(2)
        friend_buttons = self.driver.find_elements(By.XPATH, "//*[@id='sendRequest']")
        for button in friend_buttons:
            try:
                button.click()
                time.sleep(2)
                print("Friend request sent.")
            except Exception as e:
                print(f"Failed to send request: {e}")
                continue
        print("All friend requests on this page have been sent.")

    def accept_friend_requests(self):
        print("\n=== Accepting Friend Requests ===")
        self.driver.get(f"{self.live_server_url}/profile")
        self.driver.get(f"{self.live_server_url}/profile?tab=friends")
        # self.driver.find_element(By.ID, "friends").click()
        time.sleep(3)
        accept_buttons = self.driver.find_elements(By.XPATH, "//*[@id='accept']")
        for button in accept_buttons:
            try:
                button.click()
                time.sleep(2)
                print("Friend request accepted.")
            except Exception as e:
                print(f"Failed to accept request: {e}")
                continue
        print("All friend requests have been accepted.")

    def test_user_flow(self):
        self.driver.get(f"{self.live_server_url}/")
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "app")))
        time.sleep(2)
        self.signup_users()
        user1 = self.generated_users[0]
        self.login(user1['email'], user1['password'])
        # self.edit_profile(user1)
        self.age_filtering()
        self.send_friend_requests()
        self.driver.delete_all_cookies()
        user2 = self.generated_users[1]
        self.login(user2['email'], user2['password'])
        self.accept_friend_requests()
        self.driver.delete_all_cookies()
        time.sleep(3)