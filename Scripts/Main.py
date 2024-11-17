########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     12/10/2024                                                                                #
#  Purpose:  Link all the files and store the hole Machine Learning Process                            #
#                                                                                                      #
########################################################################################################


import requests                    # Package used for generating the database requests
import pandas as pd                # Importing pandas in order to use DataFrames

import ChEMBLDataExtractorMacro    # Importing the macro called "ChEMBLDataExtractorMacro.py"
import DataFilterAndPlotsMacro     # Importing the macro called "DataFilterAndPlotsMacro.py"
import ComputeChemDescriptorsMacro # Importing the macro called "ComputeChemDescriptorsMacro.py"

targetIDChEMBL       = "CHEMBL372" # Defining ChEMBL ID for COX-2, our target. 
targetProperty       = "IC50"      # Defining our target poperty
lowerTargetProperty  = -1          # Defining the lowest 'standard_value' (= targetProperty) we want to take into acount
higherTargetProperty = 200         # Defining the highest 'standard_value' (= targetProperty) we want to take into acount
percentageEresed	 = 0.2	       # Defining the percentage of the data we want to erase (number between 0 and 1)
testSizeProportion	 = 0.2         # Defining the percentage of the data we want to keep for our training set (number between 0 and 1)
randomSplitState     = 42	       # Defining the randomness for the Train/test splitting (Typically will be around 42)

ChEMBLDataExtractorMacro.ChEMBLExtractData(targetIDChEMBL, targetProperty)
dataFiles = DataFilterAndPlotsMacro.ChEMBLDataProcessingMacro(targetIDChEMBL, targetProperty,lowerTargetProperty,higherTargetProperty,
												  percentageEresed,testSizeProportion,randomSplitState)
for iFile in dataFiles : ComputeChemDescriptorsMacro.ComputeChemDescriptors(dataFiles[iFile])
