# DuoMapper
- This repo contains a series of Python scripts that organize and restructure, particularly NIH, datasets’ information and assign them GA4GH Data Use Ontology terms
- Note: make sure to keep track of which csv files the scripts are taking as input

## Script 1: organizer.py
- For Component 1A: This script reads in a csv file and writes an new csv file with the consent title column "split" so that each unique subset has its own row.

## Script 2: organizer2.py
- For Component 2A: This script reads in a "termMapping" csv file (consent titles and their corresponding PURLS) and the organized csv file outputted from organizer.py in component 1A. It will then write a new csv file with a new column adjacent to consent titles called "PURLS" that contains all the matched PURLS for a given consent title.

## Script 3: organizer3general.py
- This script searches for any general consent title in the [DOID and MONDO search system](https://www.ebi.ac.uk/ols/search?q=cancer&groupField=iri&start=0&ontology=mondo&ontology=doid) and returns the corresponding PURLs.

## Script 4: organizer3disease.py
- For Component 2B: this script parses consent titles that contain "Disease-Specific" at the start. It will then use the first term in the 
"(first term, second, third, etc.)" as the query in the [DOID and MONDO search system](https://www.ebi.ac.uk/ols/search?q=cancer&groupField=iri&start=0&ontology=mondo&ontology=doid) and return the top 5 corresponding PURLs.

## Script 5: organizer3final.py
- For Component 2B: this script looks for variations of "Disease/disorder" and "General Research Use/Health/Medical/Biomedical" in the consent title. It will then follow an algorithm and iterate through a list of terms to remove from the consent title before searching the [DOID and MONDO search system](https://www.ebi.ac.uk/ols/search?q=cancer&groupField=iri&start=0&ontology=mondo&ontology=doid) and returning the top 5 corresponding PURLs.

# Components

      1A) Task: Each semi-colon in Column I represents a unique subset of the row-level dataset. Therefore to appropriately organize the data, for
      each dataset with semicolon denoted subsets in Column I we should create an additional row with the same metadata for all fields except Column
      I, and having one of the unique terms broken up by semicolons in Column I in each row.

      Done when: There are as many dataset rows as unique entries in Column I with only one Column I subset per dataset row. 
      Mapping the Column I free text to the Data Use Ontology is cumbersome.

(Completed 2/19/2022)

---

      2A) Task: Build a script which can parse Column I and search for a list of terms (to be provided), and when a term or terms are identified,
      add a corresponding permanent Data Use Ontology URL (PURL) for each in a new column, Column J. This may involve adding multiple PURLs to a
      column.

(Completed 3/10/2022)

---

      2B) Task: Build a script which can parse Column I and search for a list of diseases (from the DOID and MONDO), and when a term or terms are
      identified, add a corresponding permanent URL (PURL) for each in a new column, Column K (DOID) and Column L (MONDO). This may involve adding
      multiple PURLs to a column.

(Completed 5/27/2022)
