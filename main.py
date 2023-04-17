from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

PATH = '/Users/karolmarszalek/chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get('https://www.kayak.com/explore/WAW-anywhere?tripdurationrange=1,10')


change_map_size = driver.find_element(By.XPATH, "//button[contains(@id, 'zoomControl-minusButton')]")
change_map_size.click()
change_map_size.click()
change_map_size.click()

wait_for_destinations = WebDriverWait(driver, 10)
while True:
    try:
        more_destinations = wait_for_destinations.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'showMoreButton')]")))
        more_destinations.click()
        sleep(1)
    except:
        break

wait_for_city_names = WebDriverWait(driver, 20)
city_names = [destination.text for destination in wait_for_city_names.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class,'City__Name')]")))]

for city_name in city_names:
    print(city_name)

driver.quit()
