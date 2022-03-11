# BroadInstitute

This repo is for the python projects that I complete for Jonathan Lawson under the supervision of Gideon Pinto. (February 18, 2022)

##Components

> 1A) Task: Each semi-colon in Column I represents a unique subset of the row-level dataset. Therefore to appropriately organize the data, for
> each dataset with semicolon denoted subsets in Column I we should create an additional row with the same metadata for all fields except Column
> I, and having one of the unique terms broken up by semicolons in Column I in each row.
> 
> Done when: There are as many dataset rows as unique entries in Column I with only one Column I subset per dataset row. 
> Mapping the Column I free text to the Data Use Ontology is cumbersome. (Completed 2/19/2022)
> 
> 2A) Task: Build a script which can parse Column I and search for a list of terms (to be provided), and when a term or terms are identified,
> add a corresponding permanent Data Use Ontology URL (PURL) for each in a new column, Column J. This may involve adding multiple PURLs to a
> column. (Completed 3/10/2022)
> 
> 2B) Task: Build a script which can parse Column I and search for a list of diseases (from the DOID and MONDO), and when a term or terms are
> identified, add a corresponding permanent URL (PURL) for each in a new column, Column K (DOID) and Column L (MONDO). This may involve adding
> multiple PURLs to a column.

##Python Scripts

> organizer.py takes in a csv file and splits the consent title column so that each unique subset has its own row.
> 
> organizer2.py reads in the termMapping csv file and the organized csv file outputted from organizer.py in component 1A.
