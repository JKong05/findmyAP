from bs4 import BeautifulSoup
import requests
import re

response = requests.get("https://apstudents.collegeboard.org/getting-credit-placement/search-policies/college/4045")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    scores = []
    page_elements = soup.find_all("div", class_="cb-table-responsive")

    for info in page_elements:
        scores.append(page_elements.text.strip())
    print(scores)