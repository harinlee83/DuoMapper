import csv

# Insert "consent title" column letter (captialized) here
row_letter = "I"
CONSENT_TITLE_ROW_NUMBER = ord(row_letter) - ord("A")

# Insert csv file names here
original_CSV_file = "DUO Validation Project - Development Dataset - Sheet1.csv"
new_CSV_file = "ORGANIZED: DUO Validation Project - Development Dataset - Sheet1.csv"

with open(original_CSV_file, "r") as originalFile:
    with open(new_CSV_file, "w") as newFile:

        reader = csv.reader(originalFile)
        writer = csv.writer(newFile)

        # Store the column headers and print them in newFile
        columnHeaders = next(reader)
        writer.writerow(columnHeaders)

        for line in reader:
            # Check to see if there are multiple subsets in "consent title" column
            if len(line[CONSENT_TITLE_ROW_NUMBER]) != 1:
                # Parse each subset into an element of an array
                Titles = line[CONSENT_TITLE_ROW_NUMBER].split(";")
                numTitles = len(Titles)
                for extraRow in range(numTitles):
                    # Make a changeable copy of current line
                    copyLine = line.copy()
                    copyLine[CONSENT_TITLE_ROW_NUMBER] = Titles[extraRow].strip()
                    writer.writerow(copyLine)
            else:
                writer.writerow(line)