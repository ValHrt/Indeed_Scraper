import requests
import time
from scraper import Scraper
from datasave import DataSave
from user_interface import UserInterface


job_name = input("Intitulé du poste : ").replace(" ", "+")
job_location = input("Lieu du poste : ").replace(" ", "+")
job_distance = input("Combien de kilomètres maximum du lieu indiqué (par tranche de 25km) : ")
job_type = input("Type de poste recherché (internship, permanent, ...) : ")

scrap = True

# user_interface = UserInterface()
scraper = Scraper(job_name, job_location, job_distance, job_type)
global_content = scraper.global_content
print(scraper.final_url)

datasave = DataSave(scraper.today.strftime("%Y-%m-%d"), job_type, job_name, job_location)

records = []

while scrap:

    for content in global_content:
        data = scraper.get_record(content, scraper.final_url)
        print(data)
        records.append(data)

    scraper.page_number += 1
    next_page = scraper.get_next_page(scraper.soup)

    if next_page == "Fin du scrapping":
        scrap = False

    else:
        scraper.response = requests.get(next_page)
        scraper.response.raise_for_status()
        scraper.final_url = scraper.response.url
        print(scraper.final_url)
        scraper.soup = scraper.scrape_html(scraper.response.text)[0]
        global_content = scraper.scrape_html(scraper.response.text)[1]
        time.sleep(5)

if len(records) > 0:
    datasave.save_to_csv(records)
else:
    print("Aucun résultat trouvé pour ces critères.")
