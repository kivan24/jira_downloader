import jira.jira as jira
import configparser
import logging
import sys


logging.basicConfig(level=logging.INFO, 
                    filename="catalina_out.log",
                    format="%(asctime)s  %(module)s %(levelname)s    %(message)s")
logging.info(f"\n\n{'*' * 16}\nStarting...\n{'*' * 16}\n")

config = configparser.ConfigParser()
config.read("settings.conf")

try:
    jira_url = config["jira"]["jira_url"]
    username = config["jira"].get("username")
    password = config["jira"].get("password")
    project_key = config["jira"]["project_key"]
    issues_folder = config["jira"]["issues_folder"]
    attachments_folder = config["jira"]["attachments_folder"]
    export_type = config["jira"]["export_type"]
except KeyError as ex:
    logging.exception("No mandatory parameters proveided " + str(ex))
    print("No mandatory parameters provided")
    sys.exit()


try:
    jira.JIRA.is_available(jira_url)
except:
    logging.exception("No connection to url ")
    print("No connection to url")
    sys.exit()


jra = jira.JIRA(jira_url, auth=(username, password), folders=(issues_folder, attachments_folder))
jra.download_all_issues_from_project(project_key, export_type)
