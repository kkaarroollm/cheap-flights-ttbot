import json

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

PATH = '/Users/karolmarszalek/chromedriver.exe'
driver = webdriver.Chrome(PATH)
# change mouse pointer cause kayak is different lol
action = ActionChains(driver)
action.move_by_offset(5, 5)
driver.maximize_window()

Warsaw = 'WAW'
Cracow = 'KRK'

driver.get(f'https://www.kayak.com/explore/{Cracow}-anywhere?tripdurationrange=1,10')


change_map_size = driver.find_element(By.XPATH, "//button[contains(@id, 'zoomControl-minusButton')]")
change_map_size.click()
change_map_size.click()
change_map_size.click()

wait_for_destinations = WebDriverWait(driver, 10)
while True:
    try:
        more_destinations = wait_for_destinations.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'showMoreButton')]")))
        more_destinations.click()
    except:
        break

sleep(2)
destinations = driver.find_elements(By.XPATH, "//div[contains(@id,'destinations')]//button")

flight_list = []
counter = 0

for button in destinations:
    flight_data = {}
    action.click(button).perform()

    wait_for_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'Explore-DestinationDetailsDrawerSection')]")))

    wait_for_info_btn = WebDriverWait(driver, 10)
    info_btn = wait_for_info_btn.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[contains(@class, 'explore-clickout-button')]")))
    flight_data['cities'] = driver.find_element(By.CLASS_NAME, 'clickout-box-title').text
    flight_data['dates'] = driver.find_element(By.CLASS_NAME, 'clickout-box-subtitle').text
    action.click(info_btn).perform()
    flight_data['link'] = info_btn.get_attribute('href')

    current_window_handle = driver.current_window_handle

    for window_handle in driver.window_handles:
        if window_handle != current_window_handle:
            driver.switch_to.window(window_handle)

    # switch window to the new
    try:
        element = driver.find_element(By.XPATH,
                                      "//h2[contains(text(), 'Security Check:')]")
        print('print human')
        driver.close()
        break
    except NoSuchElementException:
        wait_for_loaded_page = WebDriverWait(driver, 120)
        wait_for_loaded_page.until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//div[contains(@id, 'advice') and (contains(text(), '¯\_(ツ)_/¯') or contains(text(), 'Buy now'))]")
            )
        )

        wrapper_elements = wait_for_loaded_page.until(EC.visibility_of_all_elements_located(
            (By.XPATH, "//div[contains(@class, 'resultsContainer')]//div[contains(@class, 'wrapper')]")))

        cheapest_element = None
        for wrapper in wrapper_elements:
            try:
                if 'Cheapest' in wrapper.text:
                    cheapest_element = wrapper.find_element(By.XPATH, ".//*[text()='Cheapest']")
                    flight_data['price'] = wrapper.find_element(By.XPATH, ".//*[contains(@class, 'price-section')]//a").text
                    break
            except NoSuchElementException:
                pass

        flight_list.append(flight_data)
        driver.close()
        driver.switch_to.window(current_window_handle)
    close_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, "//button[contains(@data-type-id, 'Anywhere')]")))
    close_button.click()
    counter += 1

flight_dict = {"flights": flight_list}
with open(f'flight_{Cracow}.json', 'w') as f:
    json.dump(flight_dict, f, indent=2)

driver.quit()
print(counter)

