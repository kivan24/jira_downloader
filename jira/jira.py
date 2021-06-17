from jira.project import Project
from jira.issue import Issue
import time
import requests
import logging
import sys

class JIRA:
    __api_url_base = "rest/api/2/"
    __issues = []
    
    def __init__(self, url, **kwargs):
        self.__jira_url = url + ("/" if not url.endswith("/") else "")
        self.__username = kwargs["auth"][0]
        self.__password = kwargs["auth"][1]
        self.__issues_folder = kwargs["folders"][0]
        self.__attachments_folder = kwargs["folders"][1]
        self.__jira_session = requests.Session()

        if self.__username and self.__password:
            self.__jira_session.auth = (self.__username, self.__password)
            self.__login()


    def __login(self):
        """
        Try to logg-in
        """
        response = self.__jira_session.get(self.__jira_url)
        if response.status_code == requests.codes.ok:
            logging.info("Successfully logged-in")
        elif response.status_code == 401:
            logging.error("401 Unauthorized - wrong username or password")
            sys.exit()


    def download_all_issues_from_project(self, project_key, export_type):
        """
        перевіряє чи є такий проект і повертає обєкт з проектом.
        """
        self.__project = self.__get_project(project_key.upper())
        self.__get_issues(self.__project.get_search_params())
        self.__download(export_type)


    def __get_project(self, project_key):
        """Checks if project exists
        """
        url = self.__jira_url + self.__api_url_base + "project/" + project_key
        response = self.__jira_session.get(url)
        
        if response.status_code != requests.codes.ok:
            logging.exception(str(response.json()["errorMessages"]))
            response.raise_for_status()
        logging.info(f"Project {project_key} exists")
        return Project(response.json())


    def __get_issues(self, parameters):
        """
        Search for issues, and store founded issues in list
        """
        total = 1
        while parameters["startAt"] < total:
            url = self.__jira_url + self.__api_url_base + "search"
            response = self.__jira_session.get(url, params=parameters)
            response_json = response.json()
            
            for issue in response_json["issues"]:
                self.__issues.append(Issue(issue))
            
            parameters["startAt"] += parameters["maxResults"]
            total = response_json["total"]
        logging.info(f"Detected {len(self.__issues)} issues ")


    def __download(self, export_type):
        logging.info("Downloading started")
        start = time.time()
        for issue in self.__issues:
            # get issue
            logging.info(f"Downloading issue {issue.get_issue_info()}")
            url, filename = issue.download_issue(export_type)
            url = self.__jira_url + url
            response = self.__jira_session.get(url)
            self.store_to_file(filename, response.content, folder=self.__issues_folder)

            if issue.get_attachments_count():
                logging.info(f"Downloading attachments from {issue.get_issue_key()}")
                # get attachment
                url, filename = issue.download_attachments()
                url = self.__jira_url + url
                response = self.__jira_session.get(url)
                self.store_to_file(filename, response.content, folder=self.__attachments_folder)
            else:
                logging.info(f"No attachments in {issue.get_issue_key()}")
        logging.info(f"Downloading finished. Took {round(time.time() - start, 3)} seconds.\n\n")


    def store_to_file(self, filename, content, folder="./"):
        """ Store content into file
        """
        with open(folder + filename, 'wb') as file_desc:
            file_desc.write(content)


    @staticmethod
    def is_available(url):
        """Checks availability of the site
        """
        try:
            req = requests.get(url)#, verify=False)
        except:
            raise NoConnectionException("Site unavailable")
        else:
            return True
        
class NoConnectionException(Exception):
    def __init__(self, mesage):
        self.message = mesage

class ProjectSelectException(Exception):
    def __init__(self, mesage):
        self.message = mesage
