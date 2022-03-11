# Component 2: Build a script which can parse Column I and search for a list of terms (in TermMapping.csv)),
# and when a term or terms are identified, add a corresponding permanent Data Use Ontology URL (PURL) for each
# in a new column, Column J. This may involve adding multiple PURLs to a column.

# This code builds off of code from organizer.py


# Questions for Jon
# Should "Research of Any type" include any consent title that contains the word "research" in it?
# Should "Disease Specific" include any consent title that contains the word "disease" in it?

import csv

# Insert "consent title" column letter (captialized) here
consent_title_column_letter = input("Insert consent title column letter (capitalized): ")
CONSENT_TITLE_COLUMN_NUMBER = ord(consent_title_column_letter) - ord("A")

# Insert "PURL" column letter (captialized) here
PURL_title_column_letter = input("Insert column letter (capitalized) for PURLs: ")
name_of_PURL_column = input("Insert name of PURLs column: ")
PURL_COLUMN_NUMBER = ord(PURL_title_column_letter) - ord("A")

# Insert csv file names here
original_CSV_file = "ORGANIZED_v1: DUO Validation Project - Development Dataset - Test Data 2.0.csv"
new_CSV_file = "ORGANIZED_v2: DUO Validation Project - Development Dataset - Test Data 2.0.csv"
list_of_terms_CSV_file = "TermMapping.csv"

# Converts the TermMapping CSV file into a dict called mappedData to query through.
# Key = Subset Consent Title, Value = PURLs
mappedData = {}
with open(list_of_terms_CSV_file, "r") as mappingFile:
    mappedReader = csv.DictReader(mappingFile)
    for line in mappedReader:
        mappedData.setdefault(line["Query for:"],[]).append(line["If found, then add*:"].strip())

# Create dict like mappedData where all keys are uppercased
upperMappedData = {}
for key in mappedData:
    upperMappedData[key.upper()] = mappedData[key]

with open(original_CSV_file, "r") as originalFile:
    with open(new_CSV_file, "w") as newFile:

        reader = csv.reader(originalFile)
        writer = csv.writer(newFile)

        # Store the column headers, add a new PURL column, print them in newFile
        columnHeaders = next(reader)
        columnHeaders.insert(PURL_COLUMN_NUMBER,name_of_PURL_column)
        writer.writerow(columnHeaders)

        for line in reader:
            # Make a changeable copy of current line
            copyLine = line.copy()
            # Insert empty cell
            copyLine.insert(PURL_COLUMN_NUMBER,'')
            # Look for key match where capitalization variations are accounted for
            if copyLine[CONSENT_TITLE_COLUMN_NUMBER].upper() in upperMappedData or copyLine[CONSENT_TITLE_COLUMN_NUMBER].upper() + " " in upperMappedData:
                # Find subset key consent title in list of terms and insert extra cell in current line for PURL column
                key = copyLine[CONSENT_TITLE_COLUMN_NUMBER].upper()
                # Strip '[]' in the URL so it becomes a clickable link
                purl = str(upperMappedData[key]).strip("['']")
                copyLine[PURL_COLUMN_NUMBER] = purl
            # This elif is used to differentiate between General Research Use () and Disease-Specific ()
            elif "(" and "/" in copyLine[CONSENT_TITLE_COLUMN_NUMBER]:
                # Fragment consent_title by left parenthesis, comma, and white space into list of subsets
                subsets = line[CONSENT_TITLE_COLUMN_NUMBER].replace("(",",").replace(" and ",",").replace(" ",",").split(",")
                # Strip ) and , from the subsets
                for subset in range(len(subsets)):
                    subsets[subset] = subsets[subset].replace(")"," ")
                    subsets[subset] = subsets[subset].strip()
                    subsets[subset] = subsets[subset].strip().upper()
                for key in subsets:
                    if key in upperMappedData:
                        purl = str(upperMappedData[key]).strip("['']") + '\n'
                        copyLine[PURL_COLUMN_NUMBER] = copyLine[PURL_COLUMN_NUMBER] + purl
            elif "(" in copyLine[CONSENT_TITLE_COLUMN_NUMBER]:
                # Fragment consent_title by left parenthesis, comma into list of subsets
                subsets = line[CONSENT_TITLE_COLUMN_NUMBER].upper().replace("(",",").replace(" and ",",").split(",")
                # Strip ")", "USE", "ONLY"  and "," from the subsets
                for subset in range(len(subsets)):
                    subsets[subset] = subsets[subset].replace(")"," ")
                    subsets[subset] = subsets[subset].replace("USE","")
                    subsets[subset] = subsets[subset].replace("ONLY","")
                    subsets[subset] = subsets[subset].strip()
                for key in subsets:
                    if key in upperMappedData:
                        purl = str(upperMappedData[key]).strip("['']") + '\n'
                        copyLine[PURL_COLUMN_NUMBER] = copyLine[PURL_COLUMN_NUMBER] + purl
            elif "FOR" in copyLine[CONSENT_TITLE_COLUMN_NUMBER].upper():
                # Fragment consent_title by left parenthesis, comma into list of subsets
                subsets = line[CONSENT_TITLE_COLUMN_NUMBER].upper().split(",")
                # Remove "FOR", "USE", "ONLY" from the subsets
                for subset in range(len(subsets)):
                    subsets[subset] = subsets[subset].replace("FOR ","")
                    subsets[subset] = subsets[subset].replace("ONLY","")
                    subsets[subset] = subsets[subset].strip()
                for key in subsets:
                    if key in upperMappedData:
                        purl = str(upperMappedData[key]).strip("['']") + '\n'
                        copyLine[PURL_COLUMN_NUMBER] = copyLine[PURL_COLUMN_NUMBER] + purl
            elif "-" in copyLine[CONSENT_TITLE_COLUMN_NUMBER].upper():
                # Fragment consent_title by left parenthesis, comma into list of subsets
                subsets = line[CONSENT_TITLE_COLUMN_NUMBER].upper().split(" ")
                for key in subsets:
                    if key in upperMappedData:
                        purl = str(upperMappedData[key]).strip("['']") + '\n'
                        copyLine[PURL_COLUMN_NUMBER] = copyLine[PURL_COLUMN_NUMBER] + purl
            else:
                # Fragment consent_title by "ON", "AND", "WITH" and "," and - into list of subsets.
                subsets = line[CONSENT_TITLE_COLUMN_NUMBER].upper().replace(" AND ","-").replace(" ON ","-").replace(" WITH ","-").replace(",","-").split("-")
                # Strip whitespace, "USE" and "ONLY" from the subsets
                for subset in range(len(subsets)):
                    subsets[subset] = subsets[subset].replace("USE","")
                    subsets[subset] = subsets[subset].replace("ONLY","")
                    subsets[subset] = subsets[subset].strip()
                for key in subsets:
                    if key in upperMappedData:
                        purl = str(upperMappedData[key]).strip("['']") + '\n'
                        copyLine[PURL_COLUMN_NUMBER] = copyLine[PURL_COLUMN_NUMBER] + purl

            copyLine[PURL_COLUMN_NUMBER] = copyLine[PURL_COLUMN_NUMBER].strip()
            writer.writerow(copyLine)