########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     14/10/2024                                                                                #
#  Purpose:  Computing and extracting all the chemical descriptors using AlvaDesc software             #
#                                                                                                      #
########################################################################################################

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from alvadesccliwrapper.alvadesc import AlvaDesc

def ComputeChemDescriptors (dataFilePath, AlvaDescPath, silentMode = False):
    aDesc           = AlvaDesc(AlvaDescPath)                 # Importing the AlvaDesc aplication
    inputDataFrame  = pd.read_feather(dataFilePath)          # Reading the dataframe
    dataFilePath    = dataFilePath.removesuffix(".feather")  # Deleting the suffix ".feather" for later porpuses
    outputDataList  = []                                     # Generating an empty list
    if not silentMode: print("\n")
    for iSmile in tqdm(inputDataFrame["canonical_smiles"], desc=f"Computing molecular descriptors for {dataFilePath}"):
        aDesc.set_input_SMILES(iSmile)                       # Computing the descriptors
        if not aDesc.calculate_descriptors("ALL"):
            print('Error: ' + aDesc.get_error())
            pass
        outputDescriptors     = aDesc.get_output_descriptors()
        outputValues          = aDesc.get_output()[0]
        descriptorsDictionary = {'canonical_smiles' : iSmile} # Storing the descrpitors into 'descriptorsDictionary'
        # Adding the "standard_value" of each molecule
        descriptorsDictionary['standard_value'] = inputDataFrame.loc[inputDataFrame.index[inputDataFrame['canonical_smiles'] == iSmile].tolist()[0],"standard_value"]
        for iDescriptor in range(len(outputDescriptors)):
            descriptorsDictionary[outputDescriptors[iDescriptor]] = outputValues[iDescriptor]
        outputDataList.append(descriptorsDictionary)          # Adding the desciptors' dictionary to the list
    outputDataFrame = pd.DataFrame(outputDataList)            # Generating the output dataframe

    outputDataFrame.fillna(0,inplace = True)                  # Getting rid off the NaN values
    if not silentMode: print("Total of computated desciptors for each particle =  ", outputDataFrame.shape[1]-1,"\n")
    if not silentMode: print("Deleting descriptors with null values...")
    outputDataFrame = outputDataFrame.loc[:, ~(outputDataFrame == 0).all()]
    if not silentMode: print("Number of remaining chemical desciptors =           ", outputDataFrame.shape[1]-1,"\n")
    
    # Saving the data
    outputDataFrame.to_csv(f"{dataFilePath}Descriptors.csv", index = False)
    outputDataFrame.to_feather(f"{dataFilePath}Descriptors.feather")
    if not silentMode: print("The chemical descriptors have been computed and saved in" + f"{dataFilePath}Descriptors.csv")
    if not silentMode: print("The chemical descriptors have been computed and saved in" + f"{dataFilePath}Descriptors.feather\n")
    
    return outputDataFrame
