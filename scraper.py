import requests
from bs4 import BeautifulSoup
import re
import datetime as dt


class Scraper:

    def __init__(self, name: str, location: str, distance: int, j_type: str):
        self.endpoint = "https://fr.indeed.com/jobs"  # Partie à modifier pour pouvoir changer le pays
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

    def url_request(self, endpoint, parameters):
        pass