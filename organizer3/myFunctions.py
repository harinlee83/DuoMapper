# These are functions used in organizer3
# Made this module to declutter main code and so I could practice making modules :)

import requests
import json

def get_JSON(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Code: {response.status_code}, url: {url}')
    return response.text

def construct_URL(queryTerm,startNum,yesDOID):
    baseURL = "https://www.ebi.ac.uk/ols/api/search?q="
    iriURL = "&groupField=iri"

    if len(queryTerm) == 0:
        return ""

    # This refers to page numbers
    pageIndexURL = f"&start={startNum}"

    # Constructing DOID or MONDO PURLs
    if yesDOID == True:
        doidURL = "&ontology=doid"
        url = baseURL + queryTerm + iriURL + pageIndexURL + doidURL
    else:
        mondoURL = "&ontology=mondo"
        url = baseURL + queryTerm + iriURL + pageIndexURL + mondoURL
    
    return url

def get_Purl(url):

    if len(url) == 0:
        return ""

    # Initialize list and start page
    my_purls = []

    # Only get the top 5 PURLS
    numberPURLs = 5
    
    # Retireve JSON data using constructed URL
    try:
        json_Text = get_JSON(url)
        my_json = json.loads(json_Text)

        for label in my_json["response"]["docs"]:
            if len(my_purls) < numberPURLs and label["type"] == "class":
                my_purls.append(label["iri"])
    except:
        print("An exception has occured")

    return my_purls

def get_Title(url):

    if len(url) == 0:
        return ""
    
    # Initialize list and start page
    titles = []

    # Only get the top 5 PURLS
    numberPURLs = 5
    # Retireve JSON data using constructed URL
    try:
        json_Text = get_JSON(url)
        my_json = json.loads(json_Text)

        for label in my_json["response"]["docs"]:
            if len(titles) < numberPURLs and label["type"] == "class":
                titles.append(label["label"])
    except:
        print("An exception has occured")

    return titles
