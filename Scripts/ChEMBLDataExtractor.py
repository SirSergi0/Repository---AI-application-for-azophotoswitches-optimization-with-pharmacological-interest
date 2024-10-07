########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     02/10/2024                                                                                #
#  Purpose:  Import molecule's data with a known IC50 activity respect a certain protein (i.e, COX-2)  #
#                                                                                                      #
########################################################################################################

import requests
import pandas as pd


dataBaseBaseURL  = "https://www.ebi.ac.uk" # Defining the ChEMBL API web
targetIDChEMBL   = "CHEMBL372" # Defining ChEMBL ID for COX-2, our target. 
targetProperty   = "IC50" # Defining our target poperty
requestDataLimit = "1000" # The ChEMBL database has a limit of 1000 requests at the same time.
# However, we will send multimples request to extract all the data aviable.

# Setting up the query URL with the previous data
queryURL         = f"{dataBaseBaseURL}/chembl/api/data/activity.json?target_chembl_id={targetIDChEMBL}&standard_type={targetProperty}&limit={requestDataLimit}"

# Initialize a list to store all activities
allActivities   = []

# Announcing the beinning of the requesting process
print(f"Requesting data to the ChEMBL's database with the url:{queryURL}\n")

while queryURL: # Using the loop to send multiple request 
    response = requests.get(queryURL) # Getting the response for each request
    if response.status_code == 200: # Checking if the request was successful
        # Parsing the JSON response and selecting the activities (rellevant data) 
        data = response.json()
        activities = data['activities']
        allActivities.extend(activities )# Appending the activities to the list
        nextURL = data.get('page_meta', {}).get('next', None) # Gettin the URL for the next page, if it is available
        if nextURL and nextURL.startswith('/'):# If the next URL is relative, prepend the base URL
            queryURL = dataBaseBaseURL + nextURL
        else:
            queryURL = nextURL
        print(f"Fetched {len(allActivities)} total activities so far...") # Indicating the progress
    else:
        print(f"Failed to fetch data: {response.status_code}") # Printing an Error message
        break

# Printing the amount of data
print(f"\nEnd of the requesting process, we have downloaded a total of {len(allActivities)} molecule's data.")

# We want to save the data in a proper format, a Data Frame
requestedData = pd.DataFrame(allActivities) # Converting all the extracted data into a DataFrame
# Listing all the numerical variables
numericalVariables = ['activity_id','document_year','pchembl_value','record_id','src_id','standard_flag','standard_value','target_tax_id','value']
for iVariable in numericalVariables: # Converting all the numerical values to actual numbers. (Otherways they would be strings)
    requestedData[iVariable] = pd.to_numeric(requestedData[iVariable], errors='coerce')

# Removing entries with the same canonical smile
requestedData = requestedData.drop_duplicates(subset=['canonical_smiles'],keep='first')
# Removing entries with no value in the targetProperty
requestedData = requestedData.dropna(subset=['standard_value'])
requestedData = requestedData.reset_index(inplace=True) # Reseting the index of the dataframe...
print(f"Deleting molecules with the same canonical smile and no targetProperty entries. {len(requestedData)} molecule's data remaining.")

# Finding the minimum and maximum 'standard_value' indices
minimumTargetPropertyID = requestedData['standard_value'].idxmin()
maximumTargetPropertyID = requestedData['standard_value'].idxmax()

# Printing the minimum and maximum 'standard_value' and their corresponding 'standard_units'
print(f"The minimum {targetProperty} found value is {requestedData.loc[minimumTargetPropertyID, 'standard_value']} {requestedData.loc[minimumTargetPropertyID, 'standard_units']}")
print(f"The maximum {targetProperty} found value is {requestedData.loc[maximumTargetPropertyID, 'standard_value']} {requestedData.loc[maximumTargetPropertyID, 'standard_units']}")

# Save the complete dataset in an CSV file (more visual) and a Feather file (fast read/write performace)
requestedData.to_csv(f"../Data/ChEMBL_ExtractorData{targetIDChEMBL},{targetProperty},{requestDataLimit}.csv", index=False)
requestedData.to_feather(f"../Data/ChEMBL_ExtractorData{targetIDChEMBL},{targetProperty},{requestDataLimit}.feather")

# Anouncing the location of the data
print("\nData saved in the files:")
print(f"../Data/ChEMBL_ExtractorData{targetIDChEMBL},{targetProperty},{requestDataLimit}.csv")
print(f"../Data/ChEMBL_ExtractorData{targetIDChEMBL},{targetProperty},{requestDataLimit}.feather")
