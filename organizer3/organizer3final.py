# Component 2b: Build a script which can parse Column I and search for a list of diseases (from the DOID and MONDO), and when a term or terms are
# identified, add a corresponding permanent URL (PURL) for each in a new column, Column K (DOID) and Column L (MONDO). This may involve adding
# multiple PURLs to a column. It will limit PURLs to the top 5.

# This code builds off of code from organizer2.py
# This code works with Requests package and API calls to extract data from https://www.ebi.ac.uk/ols/index

import csv
from urllib.parse import quote
from numpy import true_divide
import pandas
import concurrent.futures
import re
from myFunctions import get_Purl, construct_URL, get_Title
from keywords import removeWords, keyList1, keyList2
    
def main():
    # Insert "consent title" column letter (captialized) here
    consent_title_column_letter = input("Insert consent title column letter (capitalized): ")
    CONSENT_TITLE_COLUMN_NUMBER = ord(consent_title_column_letter) - ord("A")

    SEARCH_TERM_COLUMN_NUMBER = CONSENT_TITLE_COLUMN_NUMBER + 2
    name_of_SEARCH_TERM_column = "Search Term"

    DOID_PURL_COLUMN_NUMBER = SEARCH_TERM_COLUMN_NUMBER + 1
    name_of_DOID_PURL_column = "DOID PURLs"

    DOID_TITLES_COLUMN_NUMBER = DOID_PURL_COLUMN_NUMBER + 1
    name_of_DOID_TITLE_column = "DOID Titles"

    MONDO_PURL_COLUMN_NUMBER = DOID_TITLES_COLUMN_NUMBER + 1
    name_of_MONDO_PURL_column = "MONDO PURLs"

    MONDO_TITLES_COLUMN_NUMBER = MONDO_PURL_COLUMN_NUMBER + 1
    name_of_MONDO_TITLE_column = "MONDO Titles"

    original_CSV_file = "csv files/ORGANIZED_v2: DUO Validation Project - Development Dataset - Sheet1.csv"
    new_CSV_file = "csv files/ORGANIZED_v3: DUO Validation Project - Development Dataset - Sheet1.csv"

    # Store all consent titles in an array. This will help with multi-threading later on.
    fileArray = pandas.read_csv(original_CSV_file,keep_default_na=False)
    consentTitleArray = fileArray['consent_title']

    doidPurls = []
    mondoPurls = []
    searchTerms = []

    # Default
    match1 = False
    match2 = False

    # Populate empty lists with Purls
    for item in consentTitleArray:
        # Looks for "DISEASE" or "DISORDER"
        for key1 in keyList1:
            pattern1 = re.compile(r'\b' + key1 + r'\b',re.IGNORECASE)
            matches1 = re.search(pattern1,str(item).upper())
            if matches1:
                match1 = True
                break

        # Looks for GRU or HMB
        for key2 in keyList2:
            pattern2 = re.compile(r'\b' + key2 + r'\b',re.IGNORECASE)
            matches2 = re.search(pattern2,str(item).upper())
            if matches2:
                match2 = True
                break

        # If (Disease or Disorder) OR NOT (GSU or HMB)
        if match1 or not match2:
            # Take consent title, remove list of key words and extra whitespaces
            for word in removeWords:
                pattern = re.compile(r"\b" + word + r"\b",re.IGNORECASE)
                item = re.sub(pattern,"",str(item))
            # Remove leading trailing whitespace + random punctuation
            item = re.sub(r"^\W*","",item)
            item = re.sub(r"[,/()]"," ",item)
            item = re.sub(r"\W*$","",item)
            item = re.sub(r" +"," ",item)
        else:
            # If no match, set as empty string
            item = ""
        # "Quote" ensures that the query term is URL encoded
        searchTerms.append(item)
        doidPurls.append(construct_URL(quote(item),0,True))
        mondoPurls.append(construct_URL(quote(item),0,False))

        # Reset boolean conditions
        match1 = False
        match2 = False

    # Using concurrent futures module to speed up "get requests" with threading
    with concurrent.futures.ThreadPoolExecutor() as executer:
        doidResults = list(executer.map(get_Purl, doidPurls))
        doidTitles = list(executer.map(get_Title,doidPurls))
        mondoResults = list(executer.map(get_Purl, mondoPurls))
        mondoTitles = list(executer.map(get_Title,mondoPurls))

    with open(original_CSV_file, "r") as originalFile:    
        with open(new_CSV_file, "w") as newFile:

            reader = csv.reader(originalFile)
            writer = csv.writer(newFile)

            # Store the column headers, add a new PURL column, print them in newFile
            columnHeaders = next(reader)
            columnHeaders.insert(SEARCH_TERM_COLUMN_NUMBER,name_of_SEARCH_TERM_column)
            columnHeaders.insert(DOID_PURL_COLUMN_NUMBER,name_of_DOID_PURL_column)
            columnHeaders.insert(DOID_TITLES_COLUMN_NUMBER,name_of_DOID_TITLE_column)
            columnHeaders.insert(MONDO_PURL_COLUMN_NUMBER,name_of_MONDO_PURL_column)
            columnHeaders.insert(MONDO_TITLES_COLUMN_NUMBER,name_of_MONDO_TITLE_column)
            writer.writerow(columnHeaders)

            for iterator, line in enumerate(reader):
                # Make a changeable copy of current line
                copyLine = line.copy()

                # Insert empty cell
                copyLine.insert(SEARCH_TERM_COLUMN_NUMBER,'')
                copyLine.insert(DOID_PURL_COLUMN_NUMBER,'')
                copyLine.insert(DOID_TITLES_COLUMN_NUMBER,'')
                copyLine.insert(MONDO_PURL_COLUMN_NUMBER,'')
                copyLine.insert(MONDO_TITLES_COLUMN_NUMBER,'')

                # Insert search term in file
                copyLine[SEARCH_TERM_COLUMN_NUMBER] = copyLine[SEARCH_TERM_COLUMN_NUMBER] + searchTerms[iterator] + '\n'
                copyLine[SEARCH_TERM_COLUMN_NUMBER] = copyLine[SEARCH_TERM_COLUMN_NUMBER].strip()

                # Insert DOID PURLs into file
                for purl in doidResults[iterator]:
                    copyLine[DOID_PURL_COLUMN_NUMBER] = copyLine[DOID_PURL_COLUMN_NUMBER] + purl + '\n'
                copyLine[DOID_PURL_COLUMN_NUMBER] = copyLine[DOID_PURL_COLUMN_NUMBER].strip()

                # Insert DOID Titles into file
                for title in doidTitles[iterator]:
                    copyLine[DOID_TITLES_COLUMN_NUMBER] = copyLine[DOID_TITLES_COLUMN_NUMBER] + title + '\n'
                copyLine[DOID_TITLES_COLUMN_NUMBER] = copyLine[DOID_TITLES_COLUMN_NUMBER].strip()
                            
                # Insert MONDO PURLs into file
                for purl in mondoResults[iterator]:
                    copyLine[MONDO_PURL_COLUMN_NUMBER] = copyLine[MONDO_PURL_COLUMN_NUMBER] + purl + '\n'
                copyLine[MONDO_PURL_COLUMN_NUMBER] = copyLine[MONDO_PURL_COLUMN_NUMBER].strip()

                # Insert MONDO Titles into file
                for title in mondoTitles[iterator]:
                    copyLine[MONDO_TITLES_COLUMN_NUMBER] = copyLine[MONDO_TITLES_COLUMN_NUMBER] + title + '\n'
                copyLine[MONDO_TITLES_COLUMN_NUMBER] = copyLine[MONDO_TITLES_COLUMN_NUMBER].strip()
                    
                writer.writerow(copyLine)
                iterator += 1

if __name__ == "__main__":
    main()