import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.facs.org/search/find-a-surgeon?country=United%20States&page=" 
data = pd.DataFrame([])
columns = ['name', 'specialty', 'email']

for page in range(1, 2):
        r = requests.get(base_url+ str(page))
        soup = BeautifulSoup(r.text, 'html.parser')
        all = soup.find_all("a", {"id": re.compile(r"content_element_0_main_column_1_Results_Name_[0-9]+")})

        for item in all:
            profile = item['href']
            profile_url = "https://www.facs.org" + profile

            r2 = requests.get(profile_url)
            soup2 = BeautifulSoup(r2.text, 'html.parser')
            
            name = soup2.find("h1", {"id": "content_element_0_main_column_0_ctl09_Name"}).text
            
            specialty = soup2.find("p", {"id":"content_element_0_main_column_0_ctl09_Specialty"})
            
            if specialty:
                specialty = specialty.text.replace("Specialty", "").strip()
            else:
                specialty = ""

            email = soup2.find("a", {"id": "content_element_0_main_column_0_ctl09_Email"})
            if email:
                email = email.text
            else:
                email = ""
            
            values = [name,specialty,email]

            zipped = zip(columns,values)

            data = data.append(dict(zipped), ignore_index = True)


data.to_excel(r"C:\Users\lambo\OneDrive\Documents\output.xlsx")
