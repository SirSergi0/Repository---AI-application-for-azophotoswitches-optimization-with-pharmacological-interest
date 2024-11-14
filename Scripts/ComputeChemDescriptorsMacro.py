########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     14/10/2024                                                                                #
#  Purpose:  Computing and extracting all the chemical descriptors using AlvaDesc software             #
#                                                                                                      #
########################################################################################################

import pandas as pd

from alvadesccliwrapper.alvadesc import AlvaDesc
aDesc = AlvaDesc('/Applications/alvaDesc.app/Contents/MacOS/alvaDescCLI') 


targetIDChEMBL       = "CHEMBL372" # Defining ChEMBL ID for COX-2, our target. 
targetProperty       = "IC50"      # Defining our target poperty
requestDataLimit     = 1000
dataFileName         = f"ChEMBL_ExtractorData_{targetIDChEMBL}_{targetProperty}_{requestDataLimit}"
dataFilePath         = "../Data/"
DataFrame            = pd.read_feather(dataFilePath+dataFileName+".feather")

for iSmile in DataFrame["canonical_smiles"]:
    aDesc.set_input_SMILES(iSmile)
    if not aDesc.calculate_descriptors('ALL'):
        print('Error: ' + aDesc.get_error())
        pass
    print(aDesc.get_output_descriptors())
    print(aDesc.get_output())

