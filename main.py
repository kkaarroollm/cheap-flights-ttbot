from selenium import webdriver
from selenium.common import NoSuchElementException
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
        sleep(2)
    except:
        break

wait_for_city_names = WebDriverWait(driver, 10)
for button in wait_for_city_names.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class,'Explore-GridViewItem')]//button"))):
    button.click()
    print('clicked button for destination')

    wait_for_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'Explore-DestinationDetailsDrawerSection')]")))

    wait_for_info_btn = WebDriverWait(driver, 10)
    info_btn = wait_for_info_btn.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[contains(@class, 'explore-clickout-button')]")))
    info_btn.click()
    current_window_handle = driver.current_window_handle


    # switch window to the new
    for window_handle in driver.window_handles:
        if window_handle != current_window_handle:
            driver.switch_to.window(window_handle)

    wait_for_city_names = WebDriverWait(driver, 30)
    wait_for_city_names.until(
        EC.visibility_of_element_located(
            (By.XPATH,
             "//div[contains(@id, 'advice') and (contains(text(), '¯\_(ツ)_/¯') or contains(text(), 'Buy now'))]")
        )
    )

    wrapper_elements = wait_for_city_names.until(EC.visibility_of_all_elements_located(
        (By.XPATH, "//div[contains(@class, 'resultsContainer')]//div[contains(@class, 'wrapper')]")))

    cheapest_element = None
    for wrapper in wrapper_elements:
        if 'Cheapest' in wrapper.text:
            cheapest_element = wrapper.find_element(By.XPATH, ".//*[text()='Cheapest']")
            print('*'*10)
            print(wrapper.text)
            print('*'*10)
            break

    if cheapest_element is not None:
        cheapest_element = wait_for_city_names.until(EC.visibility_of(cheapest_element))

    if cheapest_element is None:
        print("Cheapest element not found")

    driver.close()

    driver.switch_to.window(current_window_handle)
    close_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, "//button[contains(@data-type-id, 'Anywhere')]")))
    close_button.click()

    print('closed destination')


driver.quit()
