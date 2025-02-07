########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     02/10/2024                                                                                #
#  Purpose:  Import molecule's data with a known property activity respect a certain protein           #
#            (i.e, COX-2)                                                                              #
#                                                                                                      #
########################################################################################################
import requests

# Test query URL
queryURL = "https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL4523964&standard_type=IC50&limit=5"

response = requests.get(queryURL)

if response.status_code == 200:
    data = response.json()
    print("Response keys:", data.keys())  # Check top-level keys
    print("\nExample data:\n", data)  # Print full response (first few entries)
else:
    print("Request failed with status code:", response.status_code)
