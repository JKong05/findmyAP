from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import sqlite3
import os
from pathlib import Path

driver = webdriver.Chrome(service=Service())

def scraping_content(school_ids):
    connection = sqlite3.connect("school_data.db")
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS updateschool")
    cursor.execute("""
                CREATE TABLE updateschool (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT, 
                course_name TEXT, 
                min_ap_score INTEGER,
                equivalent_credit TEXT,
                location TEXT,
                url TEXT

                   )
                   """)
    
    
    for school_id in school_ids:
        try:
            url = f"https://apstudents.collegeboard.org/getting-credit-placement/search-policies/college/{school_id}"
            driver.get(url)
            
            # This will check to ensure again that the table provided by collegeboard exists
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "APCPTable")))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cb-h4')))
            
            # Extract school name
            school_name = driver.find_element(By.CLASS_NAME, 'cb-h4').text

            # Look for actual content that we need to retrieve
            courses = driver.find_elements(By.XPATH, '//table[@id="APCPTable"]/tbody/tr/th/a')
            scores = driver.find_elements(By.XPATH, '//table[@id="APCPTable"]/tbody/tr/td[1]')
            equal_credits = driver.find_elements(By.XPATH, '//table[@id="APCPTable"]/tbody/tr/td[3]')
            location_element = driver.find_element(By.XPATH, '//*[@id="APCPSearchRoot"]/div/div/div[1]/div/p[1]')
            location = location_element.text

            url = driver.find_element(By.XPATH, '//*[@id="APCPSearchRoot"]/div/div/div[1]/div/h2/a').get_attribute('href')
           
            for course, score, equal_credit in zip(courses, scores, equal_credits):
                course_name = course.text
                ap_score_text = score.text
                
                if ap_score_text.isdigit():
                    min_ap_score = int(ap_score_text)
                else:
                    min_ap_score = None

                equivalent_credit = equal_credit.text

                cursor.execute("INSERT INTO updateschool (school_name, course_name, min_ap_score, equivalent_credit, location, url) VALUES (?, ?, ?, ?, ?, ?)",
                               (school_name, course_name, min_ap_score, equivalent_credit, location, url))
            connection.commit()
        except (NoSuchElementException, TimeoutException):
            print(NoSuchElementException)
            print(TimeoutException)
            print(school_name)
            print(school_id)
            continue
        except ValueError:
            print(f"Error reported at: {school_id}")
            exit()
            
    connection.close()

def helper_function():
    school_ids = []
    for school_id in range(1, 5000):
        try:
            url = f"https://apstudents.collegeboard.org/getting-credit-placement/search-policies/college/{school_id}"
            driver.get(url)
            
            wait = WebDriverWait(driver, 3)
            wait.until(EC.presence_of_element_located((By.ID, "APCPTable")))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cb-h4')))

            school_ids.append(school_id)

        except (NoSuchElementException, TimeoutException):
            continue
    id_dict = {'school_id': school_ids}
    df = pd.DataFrame(id_dict)
    df.to_csv('ID.csv', index=False)

    return school_ids

def main():
    # can uncomment this if need to call to this function again
    # collected_ids = helper_function() 
    df = pd.read_csv('ID.csv')
    school_ids = df['school_id']
    
    # can uncomment this if need to rerurn scrape
    scraping_content(school_ids)

    driver.quit()

if __name__ == "__main__":
    main()

import os
from pathlib import Path

