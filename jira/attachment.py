class Attachment:
    def __init__(self, json):
        self.__attachment_name = json["filename"]
        self.__attachment_id = json["id"]
        self.__attachment_size = json["size"]
        self.__attachment_mime_type = json["mimeType"]
        self.__attachment_content = json["content"]
        self.__self = json["self"]

    def get_attachment_id(self):
        return self.__attachment_id

    def get_attachment_name(self):
        return self.__attachment_name

    def get_attachment_content(self):
        return self.__attachment_content