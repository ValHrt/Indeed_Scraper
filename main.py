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

global_content = soup.select(selector=".job_seen_beacon")
print(global_content)

for content in global_content:
    job_title = content.h2.getText().replace("nouveau", "")
    job_company = content.find("span", "companyName").getText()
    job_location = content.find("div", "companyLocation").getText()

    try:
        job_salary = content.find("span", "salary-snippet").getText()
    except AttributeError:
        job_salary = "Absence de données"

    try:
        post_date = (n for n in content.find("span", "date").getText() if n.isdigit())  # ne fonctionne pas
    except AttributeError:
        post_date = 0

    job_summary = content.find("li").getText()
    print(job_title)
    print(job_company)
    print(job_location)
    print(job_salary)
    print(post_date)
    print(type(post_date))
    print(job_summary)
