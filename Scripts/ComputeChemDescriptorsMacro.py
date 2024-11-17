########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     14/10/2024                                                                                #
#  Purpose:  Computing and extracting all the chemical descriptors using AlvaDesc software             #
#                                                                                                      #
########################################################################################################

import pandas as pd
from tqdm import tqdm
from alvadesccliwrapper.alvadesc import AlvaDesc

def ComputeChemDescriptors (dataFilePath):
    aDesc = AlvaDesc('/Applications/alvaDesc.app/Contents/MacOS/alvaDescCLI') 
    inputDataFrame       = pd.read_feather(dataFilePath)
    outputDataList       = []
    for iSmile in tqdm(inputDataFrame["canonical_smiles"], desc="Computing molecular descriptors: "):
        aDesc.set_input_SMILES(iSmile)
        if not aDesc.calculate_descriptors("ALL"):
            print('Error: ' + aDesc.get_error())
            pass
        outputDescriptors = aDesc.get_output_descriptors()
        outputValues = aDesc.get_output()[0]
        descriptorsDictionary = {'canonical_smiles' : iSmile} 
        for iDescriptor in range(len(outputDescriptors)):
            descriptorsDictionary[outputDescriptors[iDescriptor]] = outputValues[iDescriptor]
        outputDataList.append(descriptorsDictionary)

    outputDataFrame = pd.DataFrame(outputDataList)
    outputDataFrame.to_csv(f"{dataFilePath}Descriptors.csv", index=False)
    outputDataFrame.to_feather(f"{dataFilePath}Descriptors.feather")
    print("The chemical descriptors have been computed and saved in" + f"{dataFilePath}Descriptors.feather/csv")
    print(outputDataFrame)

