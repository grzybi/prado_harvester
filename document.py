import json

PRADO_IMG = str("https://www.consilium.europa.eu/prado/images/")


class Document:
    def __init__(self, doc_data, doc_image):
        self.id = str(doc_data).split("</a>")[0].rsplit(" ")[-1]
        self.country = self.id.split("-")[0]
        self.type = self.id.split("-")[1].split("-")[0]

        self.first_issued_from = str(doc_data).split("First issued on:")
        if len(self.first_issued_from) == 2:
            self.first_issued_from = self.first_issued_from[1].split("</p>")[0].rsplit(" ")[-1]
        else:
            self.first_issued_from = "unknown"

        self.image_front = PRADO_IMG + self.id + "/" + str(doc_image).split("image-")[1].split(".html")[0] + ".jpg"
        self.image_back = PRADO_IMG + self.id + "/" + str(doc_image).split("image-")[2].split(".html")[0] + ".jpg"

    def to_string(self):
        d = dict()
        d["country"] = self.country
        d["type"] = self.type
        d["id"] = self.id
        d["first_issued_from"] = self.first_issued_from
        d["image_front"] = self.image_front
        d["image_back"] = self.image_back
        return json.dumps(d, indent=4)
