########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     05/10/2024                                                                                #
#  Purpose:  Analyse the extracted data by ChEMBLDataExtractor.py in order to filter out irrellevant   #
#            entries                                                                                   #
#                                                                                                      #
########################################################################################################

import pandas as pd # Importing pandas in order to use DataFrames
import matplotlib.pyplot as plt # Importing matplotlib for perfoming plots

targetIDChEMBL  	 = "CHEMBL372" # Defining ChEMBL ID for COX-2, our target. 
targetProperty  	 = "IC50" # Defining our target poperty
requestDataLimit	 = "1000" # The ChEMBL database has a limit of 1000 requests at the same time.
dataFileName    	 = f"ChEMBL_ExtractorData{targetIDChEMBL},{targetProperty},{requestDataLimit}" # Defining the name of the data file 
dataFilePath     	 = "../Data/" # Defining the path where the data file is stored
plotingPath			 = "../Plots/" # Defining the path where the plots files are stored
lowerTargetProperty  = -1   # Defining the lowest 'standard_value' (= targetProperty) we want to take into acount
higherTargetProperty = 200  # Defining the highest 'standard_value' (= targetProperty) we want to take into acount

dataImported = pd.read_feather(dataFilePath+dataFileName+".feather") # Creating the datafame, using feather files for faster read/write performance

# Anouncing the previous data entries 
print(f'Number of previous entries:         {len(dataImported)}')

# Finding the minimum and maximum 'standard_value' (= targetProperty) indices for the dataImported
minimumImportedPropertyID = dataImported['standard_value'].idxmin()
maximumImportedPropertyID = dataImported['standard_value'].idxmax()

# Printing the values
print(f'Minimum {targetProperty} in the database:       {float(dataImported.loc[minimumImportedPropertyID,'standard_value'])} {dataImported.loc[minimumImportedPropertyID, 'standard_units']}')
print(f'Maximum {targetProperty} in the database:       {float(dataImported.loc[maximumImportedPropertyID,'standard_value'])} {dataImported.loc[maximumImportedPropertyID, 'standard_units']}')

# Keeping just values into a given interval. Filtering the 'dataImported' to keep only entries within the specified interval
print(f'\nKeeping just values within the interval [{lowerTargetProperty},{higherTargetProperty}]')
dataFiltered = dataImported[(dataImported['standard_value'] >= lowerTargetProperty) & (dataImported['standard_value'] <= higherTargetProperty)]

# Anouncing the filtered data entries 
print(f'Number of filtered entries:         {len(dataFiltered)}')

# Finding the minimum and maximum 'standard_value' (= targetProperty) indices for the dataFiltered
minimumFilteredPropertyID = dataFiltered['standard_value'].idxmin()
maximumFilteredPropertyID = dataFiltered['standard_value'].idxmax()
print(f'Minimum {targetProperty} in the database:       {float(dataFiltered.loc[minimumFilteredPropertyID,'standard_value'])} {dataFiltered.loc[minimumFilteredPropertyID, 'standard_units']}')
print(f'Maximum {targetProperty} in the database:       {float(dataFiltered.loc[maximumFilteredPropertyID,'standard_value'])} {dataFiltered.loc[maximumFilteredPropertyID, 'standard_units']}')

# Ploting the remaining data
plt.hist(dataFiltered['standard_value'],bins = 200)
# Adding labels and title 
plt.xlabel(f'{targetProperty},({dataFiltered.loc[maximumFilteredPropertyID, 'standard_units']})')
plt.ylabel('Number of entries')
plt.title(f'DataRepresentation{targetProperty},min_{lowerTargetProperty},max_{higherTargetProperty}')
# Saving the histogram
print(f'\nThe plot has been saved as DataRepresentation{targetProperty}min_{lowerTargetProperty}max_{higherTargetProperty}.pdf inside the Plots directory')
plt.savefig(f'{plotingPath}DataRepresentation{targetProperty}min_{lowerTargetProperty}max_{higherTargetProperty}.pdf',format='pdf')

# Save the complete dataset in an CSV file (more visual) and a Feather file (fast read/write performace)
dataFiltered.to_csv(f"{dataFilePath}{dataFileName}min_{lowerTargetProperty}max_{higherTargetProperty}Filtered.csv", index=False)
dataFiltered.to_feather(f"{dataFilePath}{dataFileName}min_{lowerTargetProperty}max_{higherTargetProperty}Filtered.feather")

# Anouncing the location of the data
print("\nFiltered data saved in the files:")
print(f"{dataFilePath}{dataFileName}min_{lowerTargetProperty}max_{higherTargetProperty}Filtered.csv")
print(f"{dataFilePath}{dataFileName}min_{lowerTargetProperty}max_{higherTargetProperty}Filtered.feather")


