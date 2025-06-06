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
from sklearn.model_selection import train_test_split # Importing the funtion "train_test_split" for spliting our data in two sets. The training set and the testing set.
import os # Importing os to check whether the computed descriptors file already exists or not.

import SplitAndPrintDataFrameMacro # Importing the macro called "SplitAndPrintDataFrameMacro.py"
from ComputeChemDescriptorsMacro import ComputeChemDescriptors # Importing the modulus for computing chemical descriptors 

def ChEMBLDataProcessingMacro(targetIDChEMBL, targetProperty, lowerTargetProperty, higherTargetProperty,
                              percentageEresed, testSizeProportion, randomSplitState, AlvaDescPath,
                              correlationMethod, correlationLimitValue,
                              requestDataLimit = "1000", dataFilePath = "../Data/", plotingPath = "../Plots/", 
                              silentMode = False):

    # Defining file name based on target and property
    dataFileName = f"ChEMBL_ExtractorData_{targetIDChEMBL}_{targetProperty}_{requestDataLimit}"

    # List of unwanted variables to be dropped from the dataset
    unwantedVariables = ['action_type', 'activity_comment', 'activity_properties', 'assay_type',
                         'assay_variant_accession', 'assay_variant_mutation', 'bao_endpoint', 'bao_format',
                         'bao_label', 'ligand_efficiency', 'potential_duplicate', 'qudt_units',
                         'standard_upper_value', 'text_value', 'toid', 'upper_value']

    # Checking if percentageEresed is a valid number
    if not (0 <= percentageEresed <= 1):
        raise ValueError("The 'percentageEresed' variable must be between 0 and 1.")

    # Checking weather the descriptors have already been computed or not 
    if not os.path.exists(dataFilePath + dataFileName + "Descriptors.feather"): 
        # Reading data from the feather file
        dataImported = pd.read_feather(dataFilePath + dataFileName + ".feather")

        # Removing unwanted variables
        for iVariable in unwantedVariables:
            if iVariable in dataImported.columns: dataImported = dataImported.drop(iVariable, axis=1)

        if not silentMode: print("\nIMPORTED DATA")
        # Printing the rellevant data from the dataImported dataframe
        SplitAndPrintDataFrameMacro.printDataFrameLenMaxMin(dataImported, targetProperty)

        # Filtering the dataset based on the target property range
        dataFiltered = dataImported[(dataImported['standard_value'] >= lowerTargetProperty) &
                                    (dataImported['standard_value'] <= higherTargetProperty)]

        if not silentMode: print("FILTERED DATA")
        # Printing the rellevant data of the dataFiltered dataframe
        SplitAndPrintDataFrameMacro.printDataFrameLenMaxMin(dataFiltered, targetProperty)
        
        # Saving the units we are working with for later porpuses
        standardUnits = dataFiltered['standard_units'].iloc[0]

        # Rewritting the raw data with the filtered data
        dataFiltered.to_csv(dataFilePath + dataFileName + ".csv", index = False)
        dataFiltered.to_feather(dataFilePath + dataFileName + ".feather")
        
        # Computing the chemical descriptors and saving the data
        dataFiltered = ComputeChemDescriptors(dataFilePath + dataFileName + ".feather",AlvaDescPath, silentMode = silentMode) 
    else:
        if not silentMode: print("The chemical descriptors have already been computed!")
        dataFiltered  = pd.read_feather(dataFilePath + dataFileName + "Descriptors.feather")
        dataFiltered  = dataFiltered[(dataFiltered['standard_value'] >= lowerTargetProperty) &
                                     (dataFiltered['standard_value'] <= higherTargetProperty)]
        dataImported  = pd.read_feather(dataFilePath + dataFileName + ".feather")
        standardUnits = dataImported['standard_units'].iloc[0]
    
    if correlationLimitValue != 0:
        # Computing the correlation coefficients with the selected method
        if not silentMode: print("Computing the correlation coefficients using", correlationMethod, "method")
        correlationDataFrame = (dataFiltered.drop('canonical_smiles', axis = 1)).corr(method = correlationMethod)['standard_value']
        if not silentMode: print("Deleting descriptors with correlation factors below ", correlationLimitValue)
        
        # ploting the correlation factors histogram
        if not silentMode: print(f"Ploting the correlation factors in ../Plots/{targetIDChEMBL}{dataFileName}CorrelationFactors.pdf")
        plt.hist(correlationDataFrame, bins=100, color='purple', range = (-1,1), label=f"Number of descriptors {dataFiltered.shape[1]-1}")
        plt.title('Correlation factors of the computed chemical descriptors')
        plt.xlabel('Correlation Values')
        plt.ylabel('Frequency')
        plt.legend()
        plt.savefig(f"../Plots/{dataFileName}CorrelationFactors.pdf", format = 'pdf')
        plt.close()

        # Deleting chemical descriptors with low correlating values
        for iDescriptor, iCorrelationValue in correlationDataFrame.items():
            if (abs(iCorrelationValue) < correlationLimitValue): dataFiltered = dataFiltered.drop(iDescriptor, axis = 1) 
        if not silentMode: print("Number of remaining chemical desciptors =           ", dataFiltered.shape[1]-1,"\n")
        
    # Computing gaps for data removal based on percentageEresed
    iSplitValueUnder, iSplitValueUpper = SplitAndPrintDataFrameMacro.findSplitDataFrame(dataFiltered, 'standard_value', percentageEresed)

    # Creating datasets for low and high activity
    dataWithGapUnder = dataFiltered[dataFiltered['standard_value'] <= iSplitValueUnder].copy()
    dataWithGapUpper = dataFiltered[dataFiltered['standard_value'] >= iSplitValueUpper].copy()

    # Assigning activity labels: low = 0, high = 1
    dataWithGapUnder.insert(1,'activity_label', 0)
    dataWithGapUpper.insert(1,'activity_label',1)

    # Combining the two datasets into one with the gap
    dataWithGapAll = pd.concat([dataWithGapUnder, dataWithGapUpper], ignore_index=True)

    if not silentMode: print("GAPED DATA")
    # Printing the rellevant data of the dataWithGapAll dataframe
    SplitAndPrintDataFrameMacro.printDataFrameLenMaxMin(dataWithGapAll, targetProperty)
    # Finding the gap values for 'standard_value' (= targetProperty)
    minimumGapPropertyID = dataWithGapUnder['standard_value'].idxmax()
    maximumGapPropertyID = dataWithGapUpper['standard_value'].idxmin()

    # Anouncing the data gap
    if not silentMode: print(f'Minimum {targetProperty} gap:                   {float(dataWithGapUnder.loc[minimumGapPropertyID,'standard_value'])} {standardUnits}')
    if not silentMode: print(f'Maximum {targetProperty} gap:                   {float(dataWithGapUpper.loc[maximumGapPropertyID,'standard_value'])} {standardUnits}')

    # Plotting the filtered data and data with gap
    plt.hist(dataFiltered['standard_value'], bins=higherTargetProperty, label='Filtered Data')
    plt.hist(dataWithGapAll['standard_value'], bins=higherTargetProperty, label='Filtered Data With Gap')

    # Adding labels, title and legend
    plt.xlabel(f'{targetProperty} ({standardUnits})')
    plt.ylabel('Number of entries')
    plt.title(f'Data Gap Representation for {targetProperty}')
    plt.legend()

    # Saving the histogram
    plotFileName = f'DataGapRepresentation{targetProperty}percentageEresed{percentageEresed*100}Gap_min_{int(dataWithGapUnder.loc[minimumGapPropertyID,'standard_value'])}Gap_max_{int(dataWithGapUpper.loc[maximumGapPropertyID,'standard_value'])}.pdf'
    plt.savefig(f'{plotingPath}{plotFileName}', format='pdf')
    plt.close() # Closing the plot
    if not silentMode: print(f'\nThe plot has been saved as {plotFileName} inside the Plots directory')

    # Saving the dataWithGapAll dataframe
    dataWithGapAllFileName = f'{dataFilePath}{dataFileName}min_{lowerTargetProperty}max_{higherTargetProperty}FilteredGap_min_{int(dataWithGapUnder.loc[minimumGapPropertyID,'standard_value'])}Gap_max_{int(dataWithGapUpper.loc[maximumGapPropertyID,'standard_value'])}'
    dataWithGapAll.to_csv(f"{dataWithGapAllFileName}.csv", index=False)
    dataWithGapAll.to_feather(f"{dataWithGapAllFileName}.feather")
    if not silentMode: print("\nFiltered data with gap is saved in the files:")
    if not silentMode: print(f"{dataWithGapAllFileName}.csv")
    if not silentMode: print(f"{dataWithGapAllFileName}.feather")

    # Anouncing the begining of the splitting proces between train set and test set
    if not silentMode: print("\nSplitting the data randomly and generating the Training/Test sets.")
    # Splitting data into training and testing sets
    dataWithGapAllFeatures = dataWithGapAll.drop('activity_label', axis=1)
    dataWithGapAllLabels = dataWithGapAll['activity_label']

    dataWithGapAllFeaturesTrain, dataWithGapAllFeaturesTest, dataWithGapAllLabelsTrain, dataWithGapAllLabelsTest = train_test_split(
        dataWithGapAllFeatures, dataWithGapAllLabels, test_size=testSizeProportion, random_state=randomSplitState, stratify=dataWithGapAllLabels
    )

    # Gathering up all the data (Features+Labels) and reseting the indexs
    dataWithGapAllTrain                   = dataWithGapAllFeaturesTrain
    dataWithGapAllTrain.insert(1,'activity_label', dataWithGapAllLabelsTrain)
    dataWithGapAllTrain.reset_index(drop = True, inplace = True)
    dataWithGapAllTest                    = dataWithGapAllFeaturesTest
    dataWithGapAllTest.insert(1,'activity_label', dataWithGapAllLabelsTest)
    dataWithGapAllTest.reset_index(drop = True, inplace = True)
    
    # Saving the train and test data
    dataWithGapAllTrain.to_csv(f"{dataFilePath}{dataWithGapAllFileName}Train.csv", index=False)
    dataWithGapAllTest.to_csv(f"{dataFilePath}{dataWithGapAllFileName}Test.csv", index=False)
    dataWithGapAllTrain.to_feather(f"{dataFilePath}{dataWithGapAllFileName}Train.feather")
    dataWithGapAllTest.to_feather(f"{dataFilePath}{dataWithGapAllFileName}Test.feather")
    
    if not silentMode: print(f"\nTrain/Test data saved as: ")
    if not silentMode: print(f"{dataWithGapAllFileName}Train.csv")
    if not silentMode: print(f"{dataWithGapAllFileName}Test.csv")
    if not silentMode: print(f"{dataWithGapAllFileName}Train.feather")
    if not silentMode: print(f"{dataWithGapAllFileName}Test.feather")
    
    return dataWithGapAllFileName, (iSplitValueUnder+iSplitValueUpper)/2
