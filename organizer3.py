# Component 2b: Build a script which can parse Column I and search for a list of diseases (from the DOID and MONDO), and when a term or terms are
# identified, add a corresponding permanent URL (PURL) for each in a new column, Column K (DOID) and Column L (MONDO). This may involve adding
# multiple PURLs to a column.

# This code builds off of code from organizer2.py

import requests

url = 'https://www.ebi.ac.uk/ols/search?q=cancer&groupField=iri&start=0&ontology=mondo&ontology=doid'
r = requests.get(url)

print(r.text)