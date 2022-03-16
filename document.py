import json


class Document:
    def __init__(self):
        self.country = ""
        self.type = None
        self.id = None
        self.first_issued_from = ""
        self.image_front = ""
        self.image_back = ""

    def to_string(self):
        d = dict()
        d["country"] = self.country
        d["type"] = self.type
        d["id"] = self.id
        d["first_issued_from"] = self.first_issued_from
        d["image_front"] = self.image_front
        d["image_back"] = self.image_back
        return json.dumps(d, indent=4)
