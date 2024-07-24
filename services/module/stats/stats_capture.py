from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
from selenium.webdriver.support.ui import Select
from helpers.selenium import take_screenshot
from selenium.webdriver.common.action_chains import ActionChains

async def get_stats_capture():
    driver = webdriver.Chrome()
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    BASEURL = 'http://127.0.0.1:8000'
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
        WebDriverWait(driver, 20).until(EC.url_matches(BASEURL))

        # Step 4 : Pengguna menekan menu Stats (View total by item)
        nav_stats_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'nav_stats_btn'))
        )
        actions = ActionChains(driver)
        actions.move_to_element(nav_stats_btn).click().perform()
        
        WebDriverWait(driver, 20).until(EC.url_contains('stats'))
        time.sleep(3)
        take_screenshot(driver, f"item_{screenshot_path}")

        # Step 5 : Pengguna memilih toogle total (View total by price)
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'toogle_total'))
        )
        select = Select(select_element)
        select.select_by_index(1) 
        
        time.sleep(3)
        take_screenshot(driver, f"price_{screenshot_path}")

        return [f"item_{screenshot_path}",f"price_{screenshot_path}"]
    except Exception as e:
        print(f'Error occurred: {e}')
    finally:
        driver.quit()