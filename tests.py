from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# Sample data for users and hobbies
test_users = [f"testuser{i}" for i in range(1, 21)]
test_hobbies = ["Reading", "Gaming", "Cooking", "Traveling", "Photography", "Painting", "Music", "Dancing", "Hiking", "Swimming"]

# 1. Account Creation / Signup
def test_signup():
    for user in test_users:
        driver.get("http://localhost:5173/signup")
        driver.find_element(By.NAME, "fullname").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(f"{user}@example.com")
        driver.find_element(By.NAME, "password").send_keys("Password123")
        driver.find_element(By.NAME, "dob").send_keys("01/01/1990")
        hobby_input = driver.find_element(By.NAME, "new_hobby")
        for hobby in test_hobbies:
            hobby_input.clear()
            hobby_input.send_keys(hobby)
            driver.find_element(By.ID, "add_hobby_button").click()
        driver.find_element(By.ID, "create_account_button").click()
        assert "Welcome" in driver.page_source
        time.sleep(1)

# 2. Login
def test_login():
    for user in test_users:
        driver.get("http://localhost:5173/login")
        driver.find_element(By.NAME, "email").send_keys(f"{user}@example.com")
        driver.find_element(By.NAME, "password").send_keys("Password123")
        driver.find_element(By.XPATH, "//button[text()='Sign In']").click()
        assert "Dashboard" in driver.page_source
        time.sleep(1)

# 3. Edit User Profile Data
def test_edit_profile():
    for user in test_users:
        driver.get("http://localhost:5173/profile")
        driver.find_element(By.NAME, "fullname").clear()
        driver.find_element(By.NAME, "fullname").send_keys(f"{user} Updated")
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys(f"updated_{user}@example.com")
        driver.find_element(By.NAME, "dob").clear()
        driver.find_element(By.NAME, "dob").send_keys("02/02/1991")
        remove_buttons = driver.find_elements(By.CLASS_NAME, "remove-hobby")
        for btn in remove_buttons:
            btn.click()
        hobby_input = driver.find_element(By.NAME, "new_hobby")
        for hobby in test_hobbies:
            hobby_input.clear()
            hobby_input.send_keys(hobby)
            driver.find_element(By.ID, "add_hobby_button").click()
        driver.find_element(By.XPATH, "//button[text()='Save Changes']").click()
        assert "Profile updated" in driver.page_source
        time.sleep(1)

# 4. Update Password
def test_update_password():
    driver.get("http://localhost:5173/profile/?tab=security")
    driver.find_element(By.NAME, "current_password").send_keys("Password123")
    driver.find_element(By.NAME, "new_password").send_keys("NewPassword123")
    driver.find_element(By.NAME, "confirm_password").send_keys("NewPassword123")
    driver.find_element(By.XPATH, "//button[text()='Update Password']").click()
    assert "Password updated" in driver.page_source
    time.sleep(1)

# 5. Filter Users by Age
def test_filter_users_by_age():
    driver.get("http://localhost:5173")
    driver.find_element(By.NAME, "min_age").send_keys("20")
    driver.find_element(By.NAME, "max_age").send_keys("25")
    driver.find_element(By.XPATH, "//button[text()='Apply Filters']").click()
    time.sleep(2)
    users = driver.find_elements(By.CLASS_NAME, "user_card")
    assert len(users) > 0, "No users found within the specified age range."

# 6. Send Friend Request
def test_send_friend_request():
    driver.get("http://localhost:5173/users")
    driver.find_element(By.NAME, "search_user").send_keys("frienduser")
    driver.find_element(By.ID, "search_button").click()
    driver.find_element(By.ID, "send_request_button").click()
    assert "Request sent" in driver.page_source

# 7. Accept Friend Request
def test_accept_friend_request():
    driver.get("http://localhost:5173/login")
    driver.find_element(By.NAME, "email").send_keys("frienduser@example.com")
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.XPATH, "//button[text()='Sign In']").click()
    driver.get("http://localhost:5173/profile/?tab=friends")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept']"))).click()
    assert "Friend added" in driver.page_source

# Run all tests
test_signup()
time.sleep(2)
test_login()
time.sleep(2)
test_edit_profile()
time.sleep(2)
test_update_password()
time.sleep(2)
test_filter_users_by_age()
time.sleep(2)
test_send_friend_request()
time.sleep(2)
test_accept_friend_request()

driver.quit()