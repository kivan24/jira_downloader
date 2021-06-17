class Issue:
    def __init__(self, json):
        self.__issue_key = json["key"]
        self.__issue_id = json["id"]
        self.__self = json["self"]
        self.__summary = json["fields"]["summary"]
        self.__attachments_count = len(json["fields"]["attachment"])
    
    def get_issue_key(self):
        return self.__issue_key

    def get_issue_name(self):
        return self.__summary

    def get_issue_info(self):
        return f"({self.__issue_key}) {self.__summary}"
    
    def get_attachments_count(self):
        return self.__attachments_count
    
    def download_issue(self, export_type):
        url = "si/jira.issueviews:issue"
        ex_type = "html"
        extension = "html"
        if export_type.lower() == "xml":
            ex_type = "xml"
            extension = "xml"
        elif export_type.lower() == "word":
            ex_type = "word"
            extension = "doc"
        
        return f"{url}-{ex_type}/{self.__issue_key}/{self.__issue_key}.{extension}", f"{self.__issue_key}.{extension}"

    def download_attachments(self):
        return f"secure/attachmentzip/{self.__issue_id}.zip", f"{self.__issue_key}.zip"
