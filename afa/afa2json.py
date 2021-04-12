"""
Fetches the latest official AFA table from website of the ministry of finance
"""
import csv
import requests
import sys


AFA_CSV_URL = (
    "https://www.bundesfinanzministerium.de/Datenportal/Daten/offene-daten/"
    + "steuern-zoelle/afa-tabellen/datensaetze/AfA-Tabelle_allgemein-verwendbare"
    + "-Anlagengueter_alphabetisch_csv.csv?__blob=publicationFile&v=3"
)
AFA_CSV_ENCODING = "ISO-8859-3"
AFA_CSV_DELIMITER = ";"


class AfaFetchError(Exception):
    pass


class Afa2Json:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def afa_csv_to_python(csv_data, delimiter):
        afa_table = csv.reader(csv_data, delimiter=delimiter)
        next(afa_table, None)  # Skip header
        next(afa_table, None)  # Skip header
        next(afa_table, None)  # Skip header
        afa_list = [
            {"title": r[0], "useful_life": r[1], "source": r[2]} for r in afa_table
        ]
        return afa_list

    @classmethod
    def from_url(
        cls, url=AFA_CSV_URL, encoding=AFA_CSV_ENCODING, delimiter=AFA_CSV_DELIMITER
    ):
        res = requests.get(url)
        res.encoding = encoding
        if not res.ok:
            raise AfaFetchError(f"Error fetching Afa-Table: {res.status_code}")
        decoded = res.content.decode("iso8859-3")
        data = cls.afa_csv_to_python(decoded.splitlines(), delimiter)
        return cls(data)


def main():

    if len(sys.argv) == 2:
        fetch_url = sys.argv[1]
    else:
        fetch_url = AFA_CSV_URL
    try:
        print(Afa2Json.from_url(fetch_url).data)
    except AfaFetchError as e:
        exit(e)


if __name__ == "__main__":
    main()
