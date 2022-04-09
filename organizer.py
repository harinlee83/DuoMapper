# Component 1: Therefore to appropriately organize the data, for each dataset with semicolon denoted subsets in Column I we
# should create an additional row with the same metadata for all fields except Column I, and having one of the 
# unique terms broken up by semicolons in Column I in each row.

import csv

# Insert "consent title" column letter (captialized) here
consent_title_column_letter = input("Insert consent title column letter (capitalized): ")
CONSENT_TITLE_COLUMN_NUMBER = ord(consent_title_column_letter) - ord("A")

# Insert csv file names here
original_CSV_file = "csv files/DUO Validation Project - Development Dataset - Test Data 2.0.csv"
new_CSV_file = "csv files/ORGANIZED_v1: DUO Validation Project - Development Dataset - Test Data 2.0.csv"

with open(original_CSV_file, "r") as originalFile:
    with open(new_CSV_file, "w") as newFile:

        reader = csv.reader(originalFile)
        writer = csv.writer(newFile)

        # Store the column headers and print them in newFile
        columnHeaders = next(reader)
        writer.writerow(columnHeaders)

        for line in reader:
            # Check to see if there are multiple subsets in "consent title" column
            if len(line[CONSENT_TITLE_COLUMN_NUMBER]) > 1:
                # Parse each subset into an element of an array
                Titles = line[CONSENT_TITLE_COLUMN_NUMBER].split(";")
                numTitles = len(Titles)
                for extraRow in range(numTitles):
                    # Make a changeable copy of current line
                    copyLine = line.copy()
                    copyLine[CONSENT_TITLE_COLUMN_NUMBER] = Titles[extraRow].strip()
                    writer.writerow(copyLine)
            else:
                writer.writerow(line)