from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from helpers.selenium import take_screenshot

async def get_stats_capture():
    driver = webdriver.Chrome()
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    BASEURL = 'http://127.0.0.1:8000/'
    # Test Data
    email = 'flazefy'
    password = 'nopass123'
    screenshot_path = f'stats_Report_{date}.png'
   
    try:
        # Step 1 : Pengguna membuka halaman login
        driver.get(f'{BASEURL}/login')

        # Step 2 : Pengguna mengisikan form login
        driver.find_element(By.ID, 'username').send_keys(email)
        driver.find_element(By.ID, 'password').send_keys(password)

        # Step 3 : Pengguna menekan button submit
        driver.find_element(By.ID, 'submit_btn').click()
        WebDriverWait(driver, 20).until(EC.url_contains(''))

        driver.find_element(By.ID, 'nav_stats_btn').click()
        WebDriverWait(driver, 20).until(EC.url_contains('stats'))
        time.sleep(3)
        take_screenshot(driver, f"item_{screenshot_path}")

        # Select the toggle total (View total by price) and take a screenshot
        select_element = driver.find_element(By.ID, 'toogle_total')
        select = Select(select_element)
        for option in select.options:
            option.selected = False
        select.select_by_index(1)
        select_element.send_keys('\n') 
        time.sleep(3)
        take_screenshot(driver, f"price_{screenshot_path}")

        return [f"item_{screenshot_path}",f"price_{screenshot_path}"]
    except Exception as e:
        print(f'Error occurred: {e}')
    finally:
        driver.quit()