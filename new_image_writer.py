import requests as req
import os

banned_dirs = [

]

banned_docs = [
    "AUT-BO-01001-recto.jpg",
    "AUT-BO-01001-verso.jpg"
    "BEL-BO-01001-verso.jpg",
    "BEL-BO-02001-verso.jpg",
    "BEL-BO-02002-verso.jpg",
    "BEL-BO-04001-verso.jpg",
    "BEL-BO-04002-verso.jpg",
    "BEL-BO-04003-verso.jpg",
    "BEL-BO-05001-verso.jpg",
    "BEL-BO-05002-verso.jpg",
    "BEL-BO-05003-verso.jpg",
    "SWE-BO-04001-recto.jpg"
]


class NewImageWriter:
    def __init__(self, folder_dst, file_dst, file_url, force):
        self.folder_dst = folder_dst
        self.file_dst = file_dst
        self.file_url = file_url
        self.force = force

        os.makedirs(folder_dst, exist_ok=True)

    def write_file(self):
        if self.file_dst not in banned_docs:
            file_name = os.path.join(self.folder_dst, self.file_dst)
            self.write_file_internal(file_name)

    def write_file_internal(self, file_name):
        if not os.path.exists(file_name) or self.force:
            r = req.get(self.file_url)
            with open(os.path.join(file_name), "wb") as outfile:
                outfile.write(r.content)
                outfile.close()
            print(f"{file_name} - downloaded.")
        else:
            print(f"{file_name} - file exists.")
