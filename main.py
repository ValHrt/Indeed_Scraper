import requests
from bs4 import BeautifulSoup
import re
import datetime as dt

endpoint = "https://fr.indeed.com/jobs"

today = dt.datetime.today()

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
final_url = response.url

soup = BeautifulSoup(response.text, "html.parser")

global_content = soup.select(selector=".job_seen_beacon")
url_content = soup.select(selector=".mosaic-provider-jobcards")  # ne fonctionne pas (tri à faire)
# print(global_content)
# print(f"{url_content}\n\n\n------------------------------------------")  # problème lié à la longueur

# print(len(global_content))
# print(len(url_content))

for content, url in zip(global_content, url_content):
    job_title = content.h2.getText().replace("nouveau", "")
    job_company = content.find("span", "companyName").getText()
    job_location = content.find("div", "companyLocation").getText()

    try:
        job_salary = content.find("span", "salary-snippet").getText()
    except AttributeError:
        job_salary = "Absence de données"

    try:
        post_date = int(re.findall("\\d+", content.find("span", "date").getText())[0])
        if post_date < 30:
            post_date = (today - dt.timedelta(days=post_date)).strftime("%Y-%m-%d")
        else:
            post_date = "Posté il y a plus de 30 jours"
    except IndexError:
        post_date = today.strftime("%Y-%m-%d")

    job_summary = content.find("div", "job-snippet").getText().strip()
    # job_url = endpoint + url.find("a", "tapItem").get("href")
    print(job_title)
    print(job_company)
    print(job_location)
    print(job_salary)
    print(post_date)
    print(job_summary)
    # print(job_url)
