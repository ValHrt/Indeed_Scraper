import csv
import os
import time


class DataSave:

    def __init__(self, scrape_date: str, job_type: str):
        self.scrape_date = scrape_date
        self.job_type = job_type

    def save_to_csv(self, location: str, records: list):
        self.create_directory(location.title())
        with open(f"Data/{location.title()}/{self.job_type}/{self.scrape_date}.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["title", "company", "location", "salary", "post_date", "summary", "url"])
            writer.writerows(records)

    def create_directory(self, location: str):
        if not os.path.isdir("Data"):
            directory = "Data"
            parent_dir = os.getcwd()
            path = os.path.join(parent_dir, directory)
            os.makedirs(path)

        if not os.path.isdir(f"Data/{location}"):
            directory2 = location
            parent_dir2 = os.path.realpath("Data")
            path2 = os.path.join(parent_dir2, directory2)
            os.makedirs(path2)

        if not os.path.isdir(f"Data/{location}/{self.job_type}"):
            directory3 = self.job_type
            parent_dir3 = os.path.realpath(f"Data/{location}")
            path3 = os.path.join(parent_dir3, directory3)
            os.makedirs(path3)
