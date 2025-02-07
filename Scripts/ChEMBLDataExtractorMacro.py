########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     02/10/2024                                                                                #
#  Purpose:  Import molecule's data with a known property activity respect a certain protein           #
#            (i.e, COX-2)                                                                              #
#                                                                                                      #
########################################################################################################

import requests # Package used for generating the database requests
import pandas as pd # Importing pandas in order to use DataFrames
import os

# Defining the funtion responsable of extracting the data
def ChEMBLExtractData(targetIDChEMBL, targetProperty, requestDataLimit=1000, saveDir="../Data", silentMode = False): 
    # Checks if the target data is already downloaded, if it is the case, do not download again
    if os.path.exists(f"{saveDir}/ChEMBL_ExtractorData_{targetIDChEMBL}_{targetProperty}_{requestDataLimit}.feather"): 
        print("The data is already downloaded!")
        return 
    dataBaseBaseURL = "https://www.ebi.ac.uk"  # Defining the ChEMBL API web
    
    # Setting up the query URL with the provided parameters
    queryURL = f"{dataBaseBaseURL}/chembl/api/data/activity.json?target_chembl_id={targetIDChEMBL}&standard_type={targetProperty}&limit={requestDataLimit}"
    
    print(queryURL)

    allActivities = []

    # Announcing the beginning of the requesting process
    if silentMode != True: print(f"Requesting data from the ChEMBL database with the URL: {queryURL}\n")

    while queryURL:
        response = requests.get(queryURL)  # Getting the response for each request
        if response.status_code == 200:  # Checking if the request was successful
            data = response.json()
            activities = data['activities']
            allActivities.extend(activities)  # Appending the activities to the list
            nextURL = data.get('page_meta', {}).get('next', None)  # Getting the next page URL, if available
            if nextURL and nextURL.startswith('/'):  # If next URL is relative, prepend the base URL
                queryURL = dataBaseBaseURL + nextURL
            else:
                queryURL = nextURL
            if silentMode != True: print(f"Fetched {len(allActivities)} total activities so far...")
        else:
            if silentMode != True: print(f"Failed to fetch data: {response.status_code}")
            break

    # Printing the amount of data
    if silentMode != True: print(f"\nEnd of the requesting process, we have downloaded a total of {len(allActivities)} molecules' data.")

    # We want to save the data in a proper format, a DataFrame
    requestedData = pd.DataFrame(allActivities)

    # Listing all the numerical variables
    numericalVariables = ['activity_id', 'document_year', 'pchembl_value', 'record_id', 'src_id', 'standard_flag',
                          'standard_value', 'target_tax_id', 'value']
    for iVariable in numericalVariables:
        requestedData[iVariable] = pd.to_numeric(requestedData[iVariable], errors='coerce')

    # Removing entries with the same canonical smile
    requestedData = requestedData.drop_duplicates(subset=['canonical_smiles'], keep='first')
    # Removing entries with no value in the targetProperty
    requestedData = requestedData.dropna(subset=['standard_value'])
    requestedData.reset_index(inplace=True, drop=True)  # Reseting the index of the dataframe
    if silentMode != True: print(f"Deleted molecules with the same canonical smile and no targetProperty entries. {len(requestedData)} molecules' data remaining.")

    # Finding the minimum and maximum 'standard_value' indices
    minimumTargetPropertyID = requestedData['standard_value'].idxmin()
    maximumTargetPropertyID = requestedData['standard_value'].idxmax()

    # Printing the minimum and maximum 'standard_value' and their corresponding 'standard_units'
    if silentMode != True: print(f"The minimum {targetProperty} found value is {requestedData.loc[minimumTargetPropertyID, 'standard_value']} {requestedData.loc[minimumTargetPropertyID, 'standard_units']}")
    if silentMode != True: print(f"The maximum {targetProperty} found value is {requestedData.loc[maximumTargetPropertyID, 'standard_value']} {requestedData.loc[maximumTargetPropertyID, 'standard_units']}")

    # Save the complete dataset in a CSV file (more visual) and a Feather file (fast read/write performance)
    csvFile     = f"{saveDir}/ChEMBL_ExtractorData_{targetIDChEMBL}_{targetProperty}_{requestDataLimit}.csv"
    featherFile = f"{saveDir}/ChEMBL_ExtractorData_{targetIDChEMBL}_{targetProperty}_{requestDataLimit}.feather"
    
    requestedData.to_csv(csvFile, index=False)
    requestedData.to_feather(featherFile)

    # Announcing the location of the data
    if silentMode != True: print("\nData saved in the files:")
    if silentMode != True: print(csvFile)
    if silentMode != True: print(featherFile)
