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

    cursor.execute("DROP TABLE IF EXISTS school")
    cursor.execute("""
                   CREATE TABLE school (
                   school_name TEXT, 
                   course_name TEXT, 
                   min_ap_score INTEGER,
                   equivalent_credit TEXT
                   )
                   """)
    
    for school_id in school_ids:
        try:
            url = f"https://apstudents.collegeboard.org/getting-credit-placement/search-policies/college/{school_id}"
            driver.get(url)
            
            # This will check to ensure again that the table provided by collegeboard exists
            wait = WebDriverWait(driver, 6)
            wait.until(EC.presence_of_element_located((By.ID, "APCPTable")))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cb-h4')))
            
            # Extract school name
            school_name = driver.find_element(By.CLASS_NAME, 'cb-h4').text

            # Look for actual content that we need to retrieve
            courses = driver.find_elements(By.XPATH, '//table[@id="APCPTable"]/tbody/tr/th/a')
            scores = driver.find_elements(By.XPATH, '//table[@id="APCPTable"]/tbody/tr/td[1]')
            equal_credits = driver.find_elements(By.XPATH, '//table[@id="APCPTable"]/tbody/tr/td[3]')

            for course, score, equal_credit in zip(courses, scores, equal_credits):
                course_name = course.text
                ap_score_text = score.text
                
                if ap_score_text.isdigit():
                    min_ap_score = int(ap_score_text)
                else:
                    min_ap_score = None

                equivalent_credit = equal_credit.text

                cursor.execute("INSERT INTO school (school_name, course_name, min_ap_score, equivalent_credit) VALUES (?, ?, ?, ?)",
                               (school_name, course_name, min_ap_score, equivalent_credit))
            connection.commit()
        except (NoSuchElementException, TimeoutException):
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
    df = pd.read_csv('scraping/ID.csv')
    school_ids = df['school_id']
    
    # can uncomment this if need to rerurn scrape
    # scraping_content(school_ids)

    driver.quit()

if __name__ == "__main__":
    main()

import os
from pathlib import Path

