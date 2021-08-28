import requests
from bs4 import BeautifulSoup

endpoint = "https://fr.indeed.com/jobs"

job_name = input("Intitulé du poste : ")
job_location = input("Lieu du poste : ")
job_distance = input("Combien de kilomètres maximum du lieu indiqué (par tranche de 25km) : ")
job_type = input("Type de poste recherché (internship, permanent, ...) : ")

parameters = {
    "q": job_name,
    "l": job_location,
    "radius": job_distance,
    "jt": job_type,
}

response = requests.get(endpoint, params=parameters)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

global_content = soup.select(selector=".jobCard_mainContent")
print(global_content)

for content in global_content:
    test = content.h2.getText().replace("nouveau", "")
    print(test)
