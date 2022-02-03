#imports here
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
#from bs4 import BeautifulSoup
#import time

driver = webdriver.Chrome('C:/Users/lambo/chromedriver.exe')
#open the webpage
driver.get("https://www.linkedin.com/")

#target username and pw
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='session_key']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='session_password']")))

#enter username and password
username.clear()
username.send_keys('lambobr1994@gmail.com')
password.clear()
password.send_keys('Aa09212219259')

#target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#We are logged in!
for page_number in range(1,101):
    search_link = 'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%2C%22101165590%22%2C%22101452733%22%2C%22104035573%22%5D&origin=FACETED_SEARCH&page='+str(page_number)+'&serviceCategory=%5B%22220%22%2C%2255800%22%2C%22441%22%2C%2250060%22%2C%221836%22%2C%2211223%22%2C%22115%22%2C%221181%22%2C%2212139%22%2C%22123%22%2C%222174%22%2C%22272%22%2C%22296%22%2C%2243715%22%2C%2244670%22%2C%22506%22%2C%22512%22%2C%22666%22%2C%2271%22%2C%22987%22%5D&sid=1m*&title=owner%20OR%20ceo%20OR%20director'

    #load the search
    driver.get(search_link)

    #wait at most 10 seconds for page to be loaded
    driver.implicitly_wait(10)
    people_list = driver.find_elements(By.XPATH,'//a[@class="app-aware-link"]')
    all = []

    for people in people_list[0::2]:
        profile_link = people.get_attribute('href')
        driver.execute_script('''window.open("","_blank");''')
        driver.switch_to.window(driver.window_handles[1])   # switch to the new tab
        driver.get(profile_link)
        driver.implicitly_wait(10)

        name = driver.find_element(By.XPATH,'//h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]').text
        industry = driver.find_element(By.XPATH,'//p[@class="truncate text-body-small"]').text

        #click contact info
        contact_info = driver.find_element(By.XPATH,'//a[@id="top-card-text-details-contact-info"]').click()
        driver.implicitly_wait(3)
        try:
            email = driver.find_element(By.XPATH, '//section[@class="pv-contact-info__contact-type ci-email"]').text
            all.append({'name': name, 'industry': industry, 'email': email})
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue

    final = pd.DataFrame.from_dict(all)
    final.to_excel(r'C:\Users\lambo\PycharmProjects\pythonProject\linkedin_list.xlsx')







