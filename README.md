# prado_harvester
This application is used for searching and downloading pictures of authentic identity and travel documents from PRADO database.

Currently supports documents from B/O category only. (Identity card / ordinary document).

By default files are downloaded only if not exists locally. Use `--force` flag to download existing files again.

```
usage: prado_eu_bo.py [-h] [--force] [--eu] [--country COUNTRY [COUNTRY ...]] [--doc-type DOC_TYPE]

Webscrapper for images from PRADO database.

optional arguments:
  -h, --help            show this help message and exit
  --force               Force downloading images
  --eu                  Scrap countries only from EU
  --country COUNTRY [COUNTRY ...]
                        Specify countries to scrap
  --doc-type DOC_TYPE   Specify document type(s) to scrap
```

Examples of usage:

```python prado_eu_bo.py --eu``` - scrap documents from European countries only.

```python prado_eu_bo.py --country AUT NZL THA``` scrap from Austria, New Zealand and Tailand.

```python prado_eu_bo.py --country SWE --force``` scrap from Sweden and force images downloading.