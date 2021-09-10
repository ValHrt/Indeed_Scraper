import csv
import os


class DataSave:

    def __init__(self, scrape_date: str, job_type: str, job_name: str, location: str):
        self.scrape_date = scrape_date
        self.job_type = job_type.title()
        self.job_name = job_name.title().replace(" ", "+")  # à voir si cette manip s'effectue dans l'UI
        self.location = location.title().replace(" ", "+")  # à voir si cette manip s'effectue dans l'UI

    def save_to_csv(self, records: list):
        self.create_directory()
        with open(f"Data/{self.location}/{self.job_type}/{self.job_name}/{self.scrape_date}.csv", "w", newline='',
                  encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["title", "company", "location", "salary", "post_date", "summary", "url"])
            writer.writerows(records)

    def create_directory(self):
        if not os.path.isdir("Data"):
            directory = "Data"
            parent_dir = os.getcwd()
            path = os.path.join(parent_dir, directory)
            os.makedirs(path)

        if not os.path.isdir(f"Data/{self.location}"):
            directory2 = self.location
            parent_dir2 = os.path.realpath("Data")
            path2 = os.path.join(parent_dir2, directory2)
            os.makedirs(path2)

        if not os.path.isdir(f"Data/{self.location}/{self.job_type}"):
            directory3 = self.job_type
            parent_dir3 = os.path.realpath(f"Data/{self.location}")
            path3 = os.path.join(parent_dir3, directory3)
            os.makedirs(path3)

        if not os.path.isdir(f"Data/{self.location}/{self.job_type}/{self.job_name}"):
            directory4 = self.job_name
            parent_dir4 = os.path.realpath(f"Data/{self.location}/{self.job_type}")
            path4 = os.path.join(parent_dir4, directory4)
            os.makedirs(path4)
