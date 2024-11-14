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
aDesc = AlvaDesc('/Applications/alvaDesc.app/Contents/MacOS/alvaDescCLI') 


targetIDChEMBL       = "CHEMBL372" # Defining ChEMBL ID for COX-2, our target. 
targetProperty       = "IC50"      # Defining our target poperty
requestDataLimit     = 1000
dataFileName         = f"ChEMBL_ExtractorData_{targetIDChEMBL}_{targetProperty}_{requestDataLimit}"
dataFilePath         = "../Data/"
inputDataFrame       = pd.read_feather(dataFilePath+dataFileName+".feather")
outputDataList       = []


for iSmile in tqdm(inputDataFrame["canonical_smiles"], desc="Computing molecular descriptors: "):
    aDesc.set_input_SMILES(iSmile)
    if not aDesc.calculate_descriptors("MW"):
        print('Error: ' + aDesc.get_error())
        pass
    output_descriptors = aDesc.get_output_descriptors()
    output_values = aDesc.get_output()
    descriptor_data = {descriptor: value for descriptor, value in zip(output_descriptors, output_values)}
    descriptor_data['canonical_smiles'] = iSmile 
    outputDataList.append(descriptor_data)

outputDataFrame = pd.DataFrame(outputDataList)
outputDataFrame.to_csv(f"{dataFilePath}{dataFileName}Descriptors.csv", index=False)
outputDataFrame.to_feather(f"{dataFilePath}{dataFileName}Descriptors.feather")
