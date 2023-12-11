from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import openpyxl
import csv

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--incognito')


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://destinationinsights.withgoogle.com/')


# Set the range of indices for css_selector
start_index = 554
end_index = 803

# Iterate through the range of indices
for index in range(start_index, end_index + 1):
    css_selector = f'#select_option_{index}'
    


    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://destinationinsights.withgoogle.com/')
    
    input_field = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/md-content[1]/md-select')
    input_field.click()
    print("input_field click")
    time.sleep(10)
    window_size = driver.get_window_size()

    # 🥰 Calculate the middle coordinates
    middle_x = window_size['width'] // 2
    middle_y = window_size['height'] // 2

    # 🥰 Use ActionChains to perform a click at the middle of the page
    actions = ActionChains(driver)
    actions.move_by_offset(middle_x, middle_y).click().perform()
    print(actions)
    # 🥰 Optional: Add a delay (e.g., sleep) to observe the effect
    time.sleep(10)

    # Click the icon
    icon_xpath = '/html/body/div[1]/div[4]/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/md-content[1]/md-select/md-select-value/span[2]'
    icon_element = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, icon_xpath))
    )
    icon_element.click()
    print("Click The Country Icon")
    time.sleep(10)

    option_element = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )

    # Scroll to the option element
    driver.execute_script("arguments[0].scrollIntoView(true);", option_element)

    # Click on the option
    option_element.click()
    print(f"Click option_element {index}")

    # Optionally, add a delay if needed
    time.sleep(10)

    # Click the submit button
    submit_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[1]/div[2]/div[2]/div/div[2]/button')
    submit_button.click()
    print("submit_button click")
    time.sleep(10)

    # Click the specified tab
    tab_xpath = '/html/body/div[1]/div[4]/div/div/div[1]/div[2]/div[4]/div/ul/li[2]/a'
    tab = driver.find_element(By.XPATH, tab_xpath)
    tab.click()

    # To wait for some time
    time.sleep(5)  # Adjust the time as needed

    # Proceed to view the results or perform additional actions
    result_element = driver.find_element(By.XPATH, '//*[@id="monitoring-global-travel-trends-content"]/div[4]/div/ul/li[2]/a')
    result_element.click()
    print(result_element)

    parent_div_xpath = '/html/body/div[1]/div[4]/div/div/div[1]/div[2]/div[4]/div/div/div[2]/div[2]/div[2]/div[2]/div[4]'
    parent_div = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, parent_div_xpath))
    )

    # Get the HTML content of the parent div
    html_content = parent_div.get_attribute('outerHTML')

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize an empty list to store table data
    table_data = []

    # Find all list items within the parent div
    list_items = soup.find_all('li', {'class': 'list-item ng-scope'})

    # 🥰👍 Iterate through each list item and extract data for each city
    for item in list_items:
        city_data = {}
        city_data['Name'] = item.find('span', {'class': 'geographic-demand__name'}).text.strip()
        city_data['Total Demand'] = item.find('span', {'class': 'geographic-demand__total'}).text.strip()

        # Append the city dictionary to the list
        table_data.append(city_data)

    # Print the resulting list of dictionaries
    for city_data in table_data:
        print(city_data)

    csv_file_path = 'geographic_demand_data.csv'

    # 🥰👍 Write data to the CSV file
    # with open(csv_file_path, 'a', newline='') as csv_file:
    #     # Check if the file is empty
    #     if csv_file.tell() == 0:
    #         # If the file is empty, use default field names
    #         fieldnames = ['Name', 'Total Demand']
    #         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #         writer.writeheader()
    #     else:
    #         # If the file is not empty, get existing field names
    #         with open(csv_file_path, 'r') as existing_file:
    #             reader = csv.reader(existing_file)
    #             # Assuming the first row contains the header
    #             fieldnames = next(reader)

    #         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    #     # Write the data
    #     for city_data in table_data:
    #         writer.writerow(city_data)

    # with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
    # # Check if the file is empty
    #     if csv_file.tell() == 0:
    #         # If the file is empty, use default field names
    #         fieldnames = ['Name', 'Total Demand']
    #         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #         writer.writeheader()
    #     else:
    #         # If the file is not empty, get existing field names
    #         with open(csv_file_path, 'r', encoding='utf-8') as existing_file:
    #             reader = csv.reader(existing_file)
    #             # Assuming the first row contains the header
    #             fieldnames = next(reader)

    #         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    #     # Write the data
    #     for city_data in table_data:
    #         writer.writerow(city_data)

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
    # Check if the file is empty
        if csv_file.tell() == 0:
            # If the file is empty, use default field names
            fieldnames = ['Name', 'Total Demand']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
        else:
            # If the file is not empty, get existing field names
            with open(csv_file_path, 'r', encoding='utf-8', errors='replace') as existing_file:
                reader = csv.reader(existing_file)
                # Assuming the first row contains the header
                fieldnames = next(reader, None)

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the data
        for city_data in table_data:
            writer.writerow(city_data)

    print(f'Data has been successfully written to {csv_file_path}')

    # Wait before starting the next iteration
    time.sleep(30) 
