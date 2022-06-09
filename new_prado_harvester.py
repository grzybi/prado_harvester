import re

import country_converter as coco
import requests as req
from bs4 import BeautifulSoup
from new_image_writer import NewImageWriter


def get_all_countries_iso3():
    cc = coco.CountryConverter()
    return [c.lower() for c in cc.data.ISO3]


def get_euro_countries_iso3():
    cc = coco.CountryConverter()
    euro = cc.data[cc.data.continent == 'Europe']
    return [c.lower() for c in euro.ISO3]


def get_eu_countries_iso3():
    cc = coco.CountryConverter()
    eu = cc.data[cc.data.EU == 'EU']
    return [c.lower() for c in eu.ISO3]


def main():
    # countries = get_all_countries_iso3()
    # countries = get_euro_countries_iso3()
    countries = get_eu_countries_iso3()

    url_prado = "https://www.consilium.europa.eu/prado"
    url_prado_lang = "/en/"
    url_prado_documents = "prado-documents/"
    url_postfix = "/all/docs-all.html"

    counter = 0
    doctype = "-B"

    for country in countries:
        url = url_prado + url_prado_lang + url_prado_documents + country + url_postfix
        response = req.get(url)

        soup = BeautifulSoup(response.text, "lxml")
        blocks = soup.find_all(attrs={"class": "doc-info-other council-link-list"})
        for block in blocks:
            strong = str(block.find("strong"))
            # print(strong)

            if str(strong).find(country.upper() + doctype) != -1:
                block = strong.split("<strong>")[1].split("</strong>")[0]
                print("BLOCK: ", block)

                url_doc = url_prado + url_prado_lang + block + "/index.html"
                print("URL_DOC", url_doc)
                response = req.get(url_doc)
                soup_doc = BeautifulSoup(response.text, "lxml")
                images = soup_doc.find_all(attrs={"id": "info-panel-header"})
                for image_container in images:
                    # print(image_container)
                    image = str(image_container.find("img"))
                    p_recto = re.compile('Image [0-9]+ of Recto')
                    m = p_recto.search(image)
                    if m is not None:
                        p_recto_id = re.compile('[0-9]+')
                        m_id = p_recto_id.search(m.group())
                        url_img = url_prado + "/images/" + block + "/" + m_id.group() + ".jpg"
                        print("URL_IMG: ", url_img)

                        image_writer = NewImageWriter("new_img", block + "-recto.jpg", url_img, True)
                        image_writer.write_file()

                        image_writer_2 = NewImageWriter("new_img_2/" + block[:6], block + "-recto.jpg", url_img, True)
                        image_writer_2.write_file()

                    p_verso = re.compile('Image [0-9]+ of Verso')
                    m = p_verso.search(image)
                    if m is not None:
                        p_verso_id = re.compile('[0-9]+')
                        m_id = p_verso_id.search(m.group())
                        url_img = url_prado + "/images/" + block + "/" + m_id.group() + ".jpg"
                        print("URL_IMG: ", url_img)

                        image_writer = NewImageWriter("new_img", block + "-verso.jpg", url_img, True)
                        image_writer.write_file()

                        image_writer_2 = NewImageWriter("new_img_2/" + block[:6], block + "-verso.jpg", url_img, True)
                        image_writer_2.write_file()
    print(counter)


if __name__ == '__main__':
    main()
