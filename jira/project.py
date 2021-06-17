class Project:
    def __init__(self, json):
        self.__project_key = json["key"]
        self.__project_id = json["id"]
        self.__project_name = json["name"]
        self.__self = json["self"]

    def get_project_key(self):
        return self.__project_key
    
    def get_search_params(self):
        return {"jql": f"project={self.__project_key} order by key", #and created > startOfMonth()
                "validateQuery": "true",
                "fields": "summary,attachment",
                "startAt": 0,
                "maxResults": 800
               }

