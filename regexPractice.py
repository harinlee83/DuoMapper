from ctypes import sizeof
import re

consent_title = "Disease-Specific (Glioma in Adults Only, GSO) GSO 123 GSO"

key = "GSO"

pattern = re.compile(r'\b' + key + r'\b')

matches = re.search(pattern,consent_title)

if matches:
    print("Found!")