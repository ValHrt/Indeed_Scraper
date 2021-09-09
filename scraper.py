import requests
from bs4 import BeautifulSoup
import re
import datetime as dt


class Scraper:

    def __init__(self, name: str, location: str, distance: str, j_type: str):
        self.today = dt.datetime.today()
        # self.endpoint = "https://ch.indeed.com/jobs"  # Fonctionne avec Indeed Suisse
        self.endpoint = "https://fr.indeed.com/jobs"  # Partie à inclure dans l'UI pour choix du pays
        self.name = name
        self.location = location
        self.distance = distance
        self.j_type = j_type
        self.parameters = {
                "q": self.name,
                "l": self.location,
                "radius": self.distance,
                "jt": self.j_type,
        }
        self.response = requests.get(self.endpoint, self.parameters)
        self.response.raise_for_status()
        self.final_url = self.response.url
        self.soup = self.scrape_html(self.response.text)[0]
        self.global_content = self.scrape_html(self.response.text)[1]
        self.page_number = 1

    @staticmethod  # Méthode à revoir notamment sur l'argument today qui peut être passé en self
    def get_record(content: BeautifulSoup, today: dt, final_url: str):
        """"Permet d'obtenir les enregistrements au format texte pour les éléments suivants :
         Titre / Nom de l'entreprise / Lieu / Salaire / Lien de l'annonce / Résumé de l'annonce.
         Cette fonction doit être intégrée dans une boucle (for loop) pour pouvoir récupérer les
         éléments de toutes les balises <a> !"""
        job_title = content.h2.getText().replace("nouveau", "")
        job_company = content.find("span", "companyName").getText()
        job_location = content.find("div", "companyLocation").getText()
        job_summary = content.find("div", "job-snippet").getText().strip().replace("\n", " ")

        try:
            job_salary = content.find("span", "salary-snippet").getText().replace("\xa0", "")
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
        record = (job_title, job_company, job_location, job_salary, post_date, job_summary, job_url)
        return record

    @staticmethod
    def scrape_html(html_text: str):
        """"Permet de créer la soupe et de sélectionner les tags dans lesquels les données
        sont contenues. Cette fonction doit être rappelée pour chaque nouvelle page à scraper.
        Attention : Dans le cas d'une nouvelle page à scraper, il faut impérativement passer
        l'argument html_text avec les données de la nouvelle page. Il faut donc modifier les
        valeurs self : exemple :
        scraper = Scraper(job_name, job_location, job_distance, job_type)
        scraper.response = requests.get(next_page)
        scraper.response.raise_for_status()
        scraper.final_url = scraper.response.url
        scraper.soup = scraper.scrape_html(scraper.response.text)[0]
        global_content = scraper.scrape_html(scraper.response.text)[1]

        Cette fonction retourne un tuple avec en 0 la soupe et en 1 les éléments sélectionnés."""
        soup = BeautifulSoup(html_text, "html.parser")
        global_content = soup.select("a[data-jk]")
        return soup, global_content

    def get_next_page(self, soup: BeautifulSoup):
        """Fonction permettant d'obtenir la page suivante sur le site Indeed.
        Elle prend pour argument la soupe de la page en cours. Cette dernière
        est accessible de la façon suivante :
        scraper = Scraper(job_name, job_location, job_distance, job_type)
        next_page = scraper.get_next_page(scraper.soup)"""
        url_tag = soup.select(f'a[aria-label="{self.page_number}"]')
        tmp = self.final_url
        for tag in url_tag:
            self.final_url = ("https://fr.indeed.com" + tag.get("href"))  # https://ch.indeed.com
        if self.final_url == tmp:
            print(f"Fin du scrapping. Nombre de pages scrapées : {self.page_number - 1}")
            return "Fin du scrapping"
        return self.final_url
