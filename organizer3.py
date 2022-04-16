# Component 2b: Build a script which can parse Column I and search for a list of diseases (from the DOID and MONDO), and when a term or terms are
# identified, add a corresponding permanent URL (PURL) for each in a new column, Column K (DOID) and Column L (MONDO). This may involve adding
# multiple PURLs to a column.

# This code builds off of code from organizer2.py
# This code uses BeautifulSoup and Requests for "web scraping" a dynamic JavaScript Website

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json

def get_JSON(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Code: {response.status_code}, url: {url}')
    return response.text

def get_Purl(queryTerm,yesDOID):
    baseURL = "https://www.ebi.ac.uk/ols/api/search?q="
    iriURL = "&groupField=iri"
    # This refers to page numbers
    start = 0
    pageIndexURL = f"&start={start}"

    doidURL = "&ontology=doid"
    mondoURL = "&ontology=mondo"

    if yesDOID == True:
        url = baseURL + queryTerm + iriURL + pageIndexURL + doidURL
    else:
        url = baseURL + queryTerm + iriURL + pageIndexURL + mondoURL

    json_Text = get_JSON(url)
    my_json = json.loads(json_Text)
    # This finds the total number of results
    maxResultNum = my_json["response"]["numFound"]
    start = my_json["response"]["start"]
    my_purls = []
    for label in my_json["response"]["docs"]:
            if label["iri"] not in my_purls:
                my_purls.append(label["iri"])

    while start < maxResultNum:
        start += 10
        pageIndexURL = f"&start={start}"
        url = baseURL + queryTerm + iriURL + pageIndexURL + doidURL
        json_Text = get_JSON(url)
        my_json = json.loads(json_Text)

        for label in my_json["response"]["docs"]:
            if label["iri"] not in my_purls:
                my_purls.append(label["iri"])
    return my_purls

def main():
    queryTerm = "ADHD"
    # This ensures that the query term is URL encoded
    queryTerm = quote(queryTerm)
    doidPurls = get_Purl(queryTerm, True)
    mondoPurls = get_Purl(queryTerm, False)

    print("MONDO Purls")
    for purl in mondoPurls:
        print(purl)

    print("DOID Purls")
    for purl in doidPurls:
        print(purl)

if __name__ == "__main__":
    main()
