import requests
import time
from scraper import Scraper
from datasave import DataSave


job_name = input("Intitulé du poste : ")
job_location = input("Lieu du poste : ")
job_distance = input("Combien de kilomètres maximum du lieu indiqué (par tranche de 25km) : ")
job_type = input("Type de poste recherché (internship, permanent, ...) : ")

scrap = True

scraper = Scraper(job_name, job_location, job_distance, job_type)
global_content = scraper.global_content
print(scraper.final_url)

datasave = DataSave(scraper.today.strftime("%Y-%m-%d"), job_type.title())

records = []

while scrap:

    for content in global_content:
        data = scraper.get_record(content, scraper.today, scraper.final_url)
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
        print(scraper.final_url)  # Fait ressortir un problème dans la redirection des liens (perte de la donnée job_name dans l'url)
        scraper.soup = scraper.scrape_html(scraper.response.text)[0]
        global_content = scraper.scrape_html(scraper.response.text)[1]
        time.sleep(5)

datasave.save_to_csv(job_location.title(), records)
