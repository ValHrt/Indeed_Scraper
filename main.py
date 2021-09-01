from scraper import Scraper


job_name = input("Intitulé du poste : ")
job_location = input("Lieu du poste : ")
job_distance = input("Combien de kilomètres maximum du lieu indiqué (par tranche de 25km) : ")
job_type = input("Type de poste recherché (internship, permanent, ...) : ")

scraper = Scraper(job_name, job_location, job_distance, job_type)

global_content = scraper.global_content

for content in global_content:
    data = scraper.get_record(content, scraper.today, scraper.final_url)
    print(data)

test = scraper.get_next_page(scraper.soup)
print(test)
