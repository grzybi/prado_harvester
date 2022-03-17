import requests as req
import os


class ImageWriter:
    def __init__(self, folder, document, force):
        self.folder = folder
        self.document = document
        self.force = force

        os.makedirs(folder, exist_ok=True)

    def write_front(self):
        file_name = os.path.join(self.folder, self.document.id + "-front.jpg")
        self.write_file(file_name)

    def write_back(self):
        file_name = os.path.join(self.folder, self.document.id + "-back.jpg")
        self.write_file(file_name)

    def write_file(self, file_name):
        if not os.path.exists(file_name) or self.force:
            r = req.get(self.document.image_front)
            with open(os.path.join(file_name), "wb") as outfile:
                outfile.write(r.content)
                outfile.close()
            print(f"{file_name} - downloaded.")
        else:
            print(f"{file_name} - file exists.")
