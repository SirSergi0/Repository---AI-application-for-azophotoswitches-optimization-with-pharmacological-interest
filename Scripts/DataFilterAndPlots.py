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
dataFilePath     	 = "../Data/"  # Defining the path where the data file is stored
plotingPath			 = "../Plots/" # Defining the path where the plots files are stored
lowerTargetProperty  = -1   # Defining the lowest 'standard_value' (= targetProperty) we want to take into acount
higherTargetProperty = 200  # Defining the highest 'standard_value' (= targetProperty) we want to take into acount
percentageEresed	 = 0.2	# Defining the percentage of the data we want to erase (number between 0 and 1)
unwantedVariables	 = ['index','action_type', 'activity_comment', 'activity_properties', 'assay_type', 'assay_variant_accession', 
						'assay_variant_mutation', 'bao_endpoint', 'bao_format', 'bao_label', 'ligand_efficiency', 'potential_duplicate',
						'qudt_units','standard_upper_value','text_value','toid','upper_value']

# Making sure that the given value for 'percentageEresed' is a number between 0 and 1
if percentageEresed<0 or percentageEresed>1:
	raise ValueError("The 'percentageEresed variable' is not properly defined")

# Defining two functions used to find the splits values
def splitDataFrameIteration (dataFrame,column,splitValue):
	upperCounter = 0; underCounter = 0
	for iData in dataFrame[column]:
		if iData >= splitValue : upperCounter+=1
		if iData <= splitValue : underCounter+=1
	return underCounter,upperCounter

def findSplitDataFrame (dataFrame,column,percentageEresed):
	iSplitValueUnder = 0
	while True:
		if splitDataFrameIteration(dataFiltered,'standard_value',iSplitValueUnder)[0]<len(dataFiltered)*(1-percentageEresed)/2:
			iSplitValueUnder+=1
		else : break
	iSplitValueUpper = iSplitValueUnder
	while True:
		if splitDataFrameIteration(dataFiltered,'standard_value',iSplitValueUpper)[0]<len(dataFiltered)*(1+percentageEresed)/2:
			iSplitValueUpper+=1
		else : break
	return iSplitValueUnder, iSplitValueUpper

dataImported = pd.read_feather(dataFilePath+dataFileName+".feather") # Creating the datafame, using feather files for faster read/write performance
# Removing unwanted data
for iVariable in unwantedVariables:
	dataImported = dataImported.drop(iVariable,axis=1)

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

# Computing the gaps
iSplitValueUnder,iSplitValueUpper = findSplitDataFrame (dataFiltered,'standard_value',percentageEresed)

# Genereting the data gap
dataWithGapUnder = dataFiltered[dataFiltered['standard_value'] <= iSplitValueUnder].copy()
dataWithGapUpper = dataFiltered[dataFiltered['standard_value'] >= iSplitValueUpper].copy()

# Labeling the compounds: high active = 1 & low active = 0
dataWithGapUnder.loc[:, 'activity_label'] = 0
dataWithGapUpper.loc[:, 'activity_label'] = 1

# Generating the main dataFrame with gap
dataWithGapAll = pd.concat([dataWithGapUnder,dataWithGapUpper], ignore_index=True)

# Anouncing the data entries without the gap
print(f'\nKeeping just the {(1-percentageEresed)*100}% of the data (gap generation)')
print(f'Number of remaning entries:         {len(dataWithGapAll)}')

# Finding the gap values for 'standard_value' (= targetProperty)
minimumGapPropertyID = dataWithGapUnder['standard_value'].idxmax()
maximumGapPropertyID = dataWithGapUpper['standard_value'].idxmin()

# Anouncing the data gap
print(f'Minimum {targetProperty} gap:                   {float(dataWithGapUnder.loc[minimumGapPropertyID,'standard_value'])} {dataWithGapUnder.loc[minimumGapPropertyID, 'standard_units']}')
print(f'Maximum {targetProperty} gap:                   {float(dataWithGapUpper.loc[maximumGapPropertyID,'standard_value'])} {dataWithGapUpper.loc[maximumGapPropertyID, 'standard_units']}')
dataWithGapAll.reset_index()


# Ploting the data
plt.hist(dataFiltered['standard_value'], bins = higherTargetProperty, label = 'Filtered Data')
plt.hist(dataWithGapAll['standard_value'], bins = higherTargetProperty, label = 'Filtered Data With Gap')
# Adding labels, title and legend
plt.xlabel(f'{targetProperty}({dataWithGapAll.loc[maximumGapPropertyID, 'standard_units']})')
plt.ylabel('Number of entries')
plt.title(f'DataGapRepresentation{targetProperty}min_{lowerTargetProperty}max_{higherTargetProperty}Gap_min_{dataWithGapUnder.loc[minimumGapPropertyID,'standard_value']}Gap_max_{dataWithGapUpper.loc[maximumGapPropertyID,'standard_value']}')
plt.legend()
# Saving the histogram
print(f'\nThe plot has been saved as DataGapRepresentation{targetProperty}percentageEresed{percentageEresed*100}Gap_min_{int(dataWithGapUnder.loc[minimumGapPropertyID,'standard_value'])}Gap_max_{int(dataWithGapUpper.loc[maximumGapPropertyID,'standard_value'])}.pdf inside the Plots directory')
plt.savefig(f'{plotingPath}DataGapRepresentation{targetProperty}percentageEresed{percentageEresed*100}Gap_min_{int(dataWithGapUnder.loc[minimumGapPropertyID,'standard_value'])}Gap_max_{int(dataWithGapUpper.loc[maximumGapPropertyID,'standard_value'])}.pdf',format='pdf')

# Saving the data
dataWithGapAll.to_csv(f"{dataFilePath}{dataFileName}min_{lowerTargetProperty}max_{higherTargetProperty}FilteredGap_min_{int(dataWithGapUnder.loc[minimumGapPropertyID,'standard_value'])}Gap_max_{int(dataWithGapUpper.loc[maximumGapPropertyID,'standard_value'])}.csv", index=False)
dataWithGapAll.to_feather(f"{dataFilePath}{dataFileName}min_{lowerTargetProperty}max_{higherTargetProperty}FilteredGap_min_{int(dataWithGapUnder.loc[minimumGapPropertyID,'standard_value'])}Gap_max_{int(dataWithGapUpper.loc[maximumGapPropertyID,'standard_value'])}.feather")

# Anouncing the location of the data gap
print("\nFiltered data with gap is saved in the files:")
print(f"{dataFilePath}{dataFileName}min_{lowerTargetProperty}max_{higherTargetProperty}FilteredGap_min_{int(dataWithGapUnder.loc[minimumGapPropertyID,'standard_value'])}Gap_max_{int(dataWithGapUpper.loc[maximumGapPropertyID,'standard_value'])}.csv")
print(f"{dataFilePath}{dataFileName}min_{lowerTargetProperty}max_{higherTargetProperty}FilteredGap_min_{int(dataWithGapUnder.loc[minimumGapPropertyID,'standard_value'])}Gap_max_{int(dataWithGapUpper.loc[maximumGapPropertyID,'standard_value'])}.feather")



