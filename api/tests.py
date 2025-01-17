from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import json
from faker import Faker

class UserFlowTest(ChannelsLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fake = Faker()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')

        cls.driver = webdriver.Chrome(options=options)
        cls.hobbies_pool = [
            "Reading", "Cooking", "Traveling", "Gaming", "Hiking", 
            "Photography", "Painting", "Music", "Gardening", "Cycling"
        ]

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def random_dob(self):
        return self.fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y")

    def generate_email(self, name):
        return name.lower().replace(" ", ".") + "@example.com"

    def signup(self):
        full_name = self.fake.name()
        email = self.generate_email(full_name)
        password = self.fake.password(length=10)
        dob = self.random_dob()
        hobbies = random.sample(self.hobbies_pool, k=random.randint(1, 10))

        self.driver.get(f"{self.live_server_url}/signup")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "name"))).send_keys(full_name)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "dob").send_keys(dob)

        for hobby in hobbies:
            hobby_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Or type a new hobby']")))
            hobby_input.clear()
            hobby_input.send_keys(hobby)
            add_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div/main/div/div/div[2]/form/div[5]/div[3]/button"))
            )
            add_button.click()
            time.sleep(0.5)

        create_account_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div/main/div/div/div[2]/form/button"))
        )
        create_account_button.click()
        time.sleep(2)

        return {"full_name": full_name, "email": email, "password": password}

    def login(self, email, password):
        self.driver.get(f"{self.live_server_url}/login")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//*[@id='app']/div/main/div/div/div[2]/form/button").click()
        time.sleep(3)

    def test_user_flow(self):
        # Step 1: Signup for two users
        user1 = self.signup()
        user2 = self.signup()

        # Step 2: Save users to file
        with open("test_users.json", "w") as file:
            json.dump([user1, user2], file, indent=4)

        # Step 3: Login as User 1
        self.login(user1['email'], user1['password'])

        # Step 4: Edit profile
        self.driver.get(f"{self.live_server_url}/profile")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "editProfile"))).click()
        time.sleep(3)  # Observe profile editing
        self.driver.find_element(By.ID, "bio").send_keys("This is an updated bio.")
        self.driver.find_element(By.XPATH, "//button[text()='Save Changes']").click()
        time.sleep(2)

        # Step 5: Filter users by age
        min_age = random.randint(18, 50)
        max_age = random.randint(min_age + 1, 60)
        self.driver.get(f"{self.live_server_url}/users")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Min']"))).send_keys(str(min_age))
        self.driver.find_element(By.XPATH, "//input[@placeholder='Max']").send_keys(str(max_age))
        self.driver.find_element(By.XPATH, "//button[text()='Apply Filters']").click()
        time.sleep(3)

        # Step 6: Send friend request to User 2
        self.driver.get(f"{self.live_server_url}/users")
        friend_request_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[@data-email='{user2['email']}']"))
        )
        friend_request_button.click()
        time.sleep(2)

        # Step 7: Logout User 1
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")
        time.sleep(3)

        # Step 8: Login as User 2
        self.login(user2['email'], user2['password'])

        # Step 9: Accept friend request
        self.driver.get(f"{self.live_server_url}/profile?tab=friendRequests")
        accept_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept']"))
        )
        accept_button.click()
        time.sleep(2)

        # Step 10: Verify friendship
        self.driver.get(f"{self.live_server_url}/profile?tab=friends")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[text()='{user1['full_name']}']"))
        )
        time.sleep(3)
