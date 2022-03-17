from bs4 import BeautifulSoup
import requests as req
import argparse
from document import Document
from image_writer import ImageWriter

PRADO = str("https://www.consilium.europa.eu/prado")


class PradoEuBo:
    def __init__(self, force, eu_only, countries, doc_types):
        country_dict = self.build_countries_dict(countries, eu_only)
        documents = self.build_documents_list(country_dict)

        for i, d in enumerate(documents):
            print(f"\nDocument {i + 1}/{len(documents)}")
            image_writer = ImageWriter("img", d, force)
            image_writer.write_front()
            image_writer.write_back()

    @staticmethod
    def build_countries_dict(countries, eu_only):
        response = req.get(PRADO + "/en/search-by-document-country.html")
        soup = BeautifulSoup(response.text, "lxml")
        countries_blocks = soup.find_all(attrs={"class": "council-link-list"})
        country_dict = dict()

        if countries:
            country_dict = dict([(c.upper(), c.capitalize()) for c in countries[0]])
        else:
            for block in countries_blocks[:2] if eu_only else countries_blocks:
                country_link = block.find_all("a")
                for country in country_link:
                    country_name = country.text.split("-")[1]
                    country_name = country_name.split(" * ")[1].split(" *")[0] if "*" in country_name \
                        else country_name.split(" ")[1]
                    country_dict[str(country.text.split(" -")[0])] = country_name

        return country_dict

    @staticmethod
    def build_documents_list(country_dict):
        documents = list()
        # TODO: add selecting type of document(s)
        for c in country_dict:
            print(c)
            # TODO: needs to investigate what is wrong with PSE
            if c == "PSE":
                continue

            site = PRADO + "/en/prado-documents/" + str(c) + "/B/O/docs-per-type.html"
            response = req.get(site)
            soup = BeautifulSoup(response.text, "lxml")
            searching = soup.find_all(attrs={"id": "prado-top"})
            if searching:
                document_data = searching[0].find_all(attrs={"class": "doc-info col-sm-8"})
                document_images = searching[0].find_all(attrs={"class": "doc-thumbnails col-sm-4"})

                for i, doc in enumerate(document_data):
                    document = Document(doc, document_images[i])
                    print(document.to_string())
                    documents.append(document)
            else:
                print("!!! NOTHING FOUND FOR: " + c)

        return documents


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Webscrapper for images from PRADO database.")
    parser.add_argument('--force', help="Force downloading images", action="store_true")
    parser.add_argument('--eu', help="Scrap countries only from EU", action="store_true")
    parser.add_argument('--country', help="Specify countries to scrap", action="append", nargs="+", type=str)
    parser.add_argument('--doc-type', help="Specify document type(s) to scrap", action="append")
    args = parser.parse_args()

    prado = PradoEuBo(args.force, args.eu, args.country, args.doc_type)
