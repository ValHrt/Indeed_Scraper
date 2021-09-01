import requests
from bs4 import BeautifulSoup
import re
import datetime as dt


class Scraper:

    def __init__(self, name: str, location: str, distance: str, j_type: str):
        self.today = dt.datetime.today()
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

    @staticmethod
    def get_record(content: BeautifulSoup, today: dt, final_url: str):
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
        soup = BeautifulSoup(html_text, "html.parser")
        global_content = soup.select("a[data-jk]")
        return soup, global_content

    def get_next_page(self, soup: BeautifulSoup):
        url_tag = soup.select('a[aria-label="Suivant"]')
        tmp = self.final_url
        for tag in url_tag:
            self.final_url = self.endpoint + tag.get("href")
        if self.final_url == tmp:
            return "Fin du scrapping"
        return self.final_url
