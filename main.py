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

global_content = soup.select("a[data-jk]")
# print(global_content)

for content in global_content:
    job_title = content.h2.getText().replace("nouveau", "")
    job_company = content.find("span", "companyName").getText()
    job_location = content.find("div", "companyLocation").getText()
    job_summary = content.find("div", "job-snippet").getText().strip()

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

    try:
        job_url = final_url + "&advn=" + content.get("data-empn") + "&vjk=" + content.get("data-jk")
    except TypeError:
        job_url = final_url + "&vjk=" + content.get("data-jk")

    print(job_title)
    print(job_company)
    print(job_location)
    print(job_salary)
    print(post_date)
    print(job_summary)
    print(job_url)
