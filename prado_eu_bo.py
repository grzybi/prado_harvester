from bs4 import BeautifulSoup
import requests as req
from document import Document
# import itertools
import os

PRADO = str("https://www.consilium.europa.eu/prado")


class PradoEuBo:
    def __init__(self):
        response = req.get(PRADO + "/en/search-by-document-country.html")
        soup = BeautifulSoup(response.text, "lxml")
        countries_block = soup.find_all(attrs={"class": "council-link-list"})
        print(type(countries_block))
        country_list = dict()

        print(len(countries_block))
        for block in countries_block:
            countries = block.find_all("a")
            for country in countries:
                country_name = country.text.split("-")[1]
                country_name = country_name.split(" * ")[1].split(" *")[0] if "*" in country_name \
                    else country_name.split(" ")[1]
                country_list[str(country.text.split(" -")[0])] = country_name

        print(country_list)
        # print(len(country_list))

        documents = list()

        # TODO: check slicing
        # for c in ["PRK"]:
        for c in country_list:
            print(c)
            if c == "PSE":
                continue
        # for c in dict(itertools.islice(country_list.items(), 3)):
            s = PRADO + "/en/prado-documents/" + str(c) + "/B/O/docs-per-type.html"
            # print(s)
            response = req.get(s)
            soup = BeautifulSoup(response.text, "lxml")
            searching = soup.find_all(attrs={"id": "prado-top"})
            if searching:
                document_datas = searching[0].find_all(attrs={"class": "doc-info col-sm-8"})
                document_images = searching[0].find_all(attrs={"class": "doc-thumbnails col-sm-4"})

                for i, doc in enumerate(document_datas):
                    document = Document()
                    document.id = str(doc).split("</a>")[0].rsplit(" ")[-1]
                    document.country = document.id.split("-")[0]
                    document.type = document.id.split("-")[1].split("-")[0]
                    document.first_issued_from = str(doc).split("First issued on:")

                    if len(document.first_issued_from) == 2:
                        document.first_issued_from = document.first_issued_from[1].split("</p>")[0].rsplit(" ")[-1]
                    else:
                        print("!!!" + document.id)
                        document.first_issued_from = "unknown"

                    document.image_front = PRADO + "/images/" + document.id + "/" + \
                        str(document_images[i]).split("image-")[1].split(".html")[0] + ".jpg"
                    document.image_back = PRADO + "/images/" + document.id + "/" + \
                        str(document_images[i]).split("image-")[2].split(".html")[0] + ".jpg"

                    # print(document.to_string())

                    # parsed = json.dumps(json.loads(document.to_string()), indent=4)
                    # print(parsed)

                    documents.append(document)
                # print(searching)
            else:
                print("!!! NOTHING FOUND FOR: " + c)

        os.makedirs("img", exist_ok=True)

        for i, d in enumerate(documents):
            r = req.get(d.image_front)
            with open(os.path.join("img", d.id + "-front.jpg"), "wb") as outfile:
                outfile.write(r.content)
                outfile.close()

            r = req.get(d.image_back)
            with open(os.path.join("img", d.id + "-back.jpg"), "wb") as outfile:
                outfile.write(r.content)
                outfile.close()

            print(f"{i + 1}/{len(documents)}")


if __name__ == "__main__":
    prado = PradoEuBo()
