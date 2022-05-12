# Component 2b: Build a script which can parse Column I and search for a list of diseases (from the DOID and MONDO), and when a term or terms are
# identified, add a corresponding permanent URL (PURL) for each in a new column, Column K (DOID) and Column L (MONDO). This may involve adding
# multiple PURLs to a column. It will limit PURLs to the top 5.

# This code builds off of code from organizer2.py
# This code works with Requests package and API calls to extract data from https://www.ebi.ac.uk/ols/index

import csv
import requests
from urllib.parse import quote
import json
import re

RESULTS_PER_PAGE = 10

def get_JSON(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Code: {response.status_code}, url: {url}')
    return response.text

def construct_URL(queryTerm,startNum,yesDOID):
    baseURL = "https://www.ebi.ac.uk/ols/api/search?q="
    iriURL = "&groupField=iri"

    # This refers to page numbers
    pageIndexURL = f"&start={startNum}"

    doidURL = "&ontology=doid"
    mondoURL = "&ontology=mondo"

    # Constructing DOID or MONDO PURLs
    if yesDOID == True:
        url = baseURL + queryTerm + iriURL + pageIndexURL + doidURL
    else:
        url = baseURL + queryTerm + iriURL + pageIndexURL + mondoURL
    
    return url

def get_Purl(queryTerm, yesDOID):

    url = construct_URL(queryTerm,0,yesDOID)

    # Retireve JSON data using constructed URL
    json_Text = get_JSON(url)
    my_json = json.loads(json_Text)

    # This finds the total number of results
    maxResultNum = my_json["response"]["numFound"]
    
    # Initialize list and start page
    my_purls = []

    start = 0
    pageIndexURL = f"&start={start}"

    # Only get the top 5 PURLS
    numberPURLs = 1
    url = construct_URL(queryTerm,start,yesDOID)
    json_Text = get_JSON(url)
    my_json = json.loads(json_Text)

    for label in my_json["response"]["docs"]:
        if len(my_purls) < numberPURLs and label["type"] == "class":
            my_purls.append(label["short_form"])

    return my_purls

def main():

    # Insert "consent title" column letter (captialized) here
    consent_title_column_letter = input("Insert consent title column letter (capitalized): ")
    CONSENT_TITLE_COLUMN_NUMBER = ord(consent_title_column_letter) - ord("A")

    # Insert "DOID PURL" column letter (captialized) here
    doid_purl_column_letter = input("Insert DOID PURL column letter (capitalized): ")
    DOID_PURL_COLUMN_NUMBER = ord(doid_purl_column_letter) - ord("A")
    name_of_DOID_PURL_column = "DOID PURLs"

    # Insert "MONDO PURL" column letter (captialized) here
    mondo_purl_column_letter = input("Insert MONDO PURL column letter (capitalized): ")
    MONDO_PURL_COLUMN_NUMBER = ord(mondo_purl_column_letter) - ord("A")
    name_of_MONDO_PURL_column = "MONDO PURLs"

    original_CSV_file = "csv files/ORGANIZED_v2: DUO Validation Project - Development Dataset - Test Data 2.0.csv"
    new_CSV_file = "csv files/ORGANIZED_v3: DUO Validation Project - Development Dataset - Test Data 2.0.csv"

    with open(original_CSV_file, "r") as originalFile:
        with open(new_CSV_file, "w") as newFile:

            reader = csv.reader(originalFile)
            writer = csv.writer(newFile)

            # Store the column headers, add a new PURL column, print them in newFile
            columnHeaders = next(reader)
            columnHeaders.insert(DOID_PURL_COLUMN_NUMBER,name_of_DOID_PURL_column)
            columnHeaders.insert(MONDO_PURL_COLUMN_NUMBER,name_of_MONDO_PURL_column)
            writer.writerow(columnHeaders)

            iterator = 0
            totalLines = 3756

            for line in reader:
                iterator += 1
                print(f"Line {iterator} of {totalLines}")
                # Make a changeable copy of current line
                copyLine = line.copy()

                # Insert empty cell
                copyLine.insert(DOID_PURL_COLUMN_NUMBER,'')
                copyLine.insert(MONDO_PURL_COLUMN_NUMBER,'')

                queryTerm = copyLine[CONSENT_TITLE_COLUMN_NUMBER]

                list = ["DISEASE", "SPECIFIC"]
                # Looks for "DISEASE SPECIFIC" or "DISEASE-SPECIFIC"
                pattern = re.compile(r'^' + list[0] + r'[ -]' + list[1] + r'[ \(|\()]')
                matches = re.search(pattern,queryTerm.upper())

                if len(queryTerm) != 0 and matches:
                    # This finds the first term in parenthesis in a non-greedy fashion
                    parenthesisPattern = re.compile(r'\((.*?)[\,\)]')
                    result = re.search(parenthesisPattern,queryTerm)
                    try:
                        queryTerm = result.group(1)
                        # This ensures that the query term is URL encoded
                        queryTerm = quote(queryTerm)
                        doidPurls = get_Purl(queryTerm, True)
                        mondoPurls = get_Purl(queryTerm, False)

                        baseURL = "http://purl.obolibrary.org/obo/"
                        # Insert DOID PURLs into file
                        for purl in doidPurls:
                            copyLine[DOID_PURL_COLUMN_NUMBER] = copyLine[DOID_PURL_COLUMN_NUMBER] + baseURL + purl + '\n'
                        copyLine[DOID_PURL_COLUMN_NUMBER] = copyLine[DOID_PURL_COLUMN_NUMBER].strip()
                        
                        # Insert MONDO PURLs into file
                        for purl in mondoPurls:
                            copyLine[MONDO_PURL_COLUMN_NUMBER] = copyLine[MONDO_PURL_COLUMN_NUMBER] + baseURL + purl + '\n'
                        copyLine[MONDO_PURL_COLUMN_NUMBER] = copyLine[MONDO_PURL_COLUMN_NUMBER].strip()
                    except:
                        copyLine[DOID_PURL_COLUMN_NUMBER] = None
                        copyLine[MONDO_PURL_COLUMN_NUMBER] = None
                writer.writerow(copyLine)

if __name__ == "__main__":
    main()
