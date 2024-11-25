########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     12/10/2024                                                                                #
#  Purpose:  Link all the files and store the hole Machine Learning Process                            #
#                                                                                                      #
########################################################################################################

import ChEMBLDataExtractorMacro    # Importing the macro called "ChEMBLDataExtractorMacro.py"
import DataFilterAndPlotsMacro     # Importing the macro called "DataFilterAndPlotsMacro.py"

targetIDChEMBL       = "CHEMBL372" # Defining ChEMBL ID for COX-2, our target. 
targetProperty       = "IC50"      # Defining our target poperty
lowerTargetProperty  = -1          # Defining the lowest 'standard_value' (= targetProperty) we want to take into acount
higherTargetProperty = 200         # Defining the highest 'standard_value' (= targetProperty) we want to take into acount
percentageEresed	 = 0.2	       # Defining the percentage of the data we want to erase (number between 0 and 1)
testSizeProportion	 = 0.2         # Defining the percentage of the data we want to keep for our training set (number between 0 and 1)
randomSplitState     = 42	       # Defining the randomness for the Train/test splitting (Typically will be around 42)

# Pointing at the directori of the AlvaDesc instalation
AlvaDescPath		 = '/Applications/alvaDesc.app/Contents/MacOS/alvaDescCLI'

correlationMethod    = 'pearson'   # Setting up the computing correlation method to distinguish between related/non-relatied data
                                   # the accepted values are: 'pearson', 'kendall' and 'spearman'
correlationLimitValue= 0           # Setting up the (absolute) value upon (under) which the chemical descriptors will be considered to 
                                   # have a relation with the protein inhibition

ChEMBLDataExtractorMacro.ChEMBLExtractData(targetIDChEMBL, targetProperty)
DataFilterAndPlotsMacro.ChEMBLDataProcessingMacro(targetIDChEMBL, targetProperty,lowerTargetProperty,higherTargetProperty,
                                                  percentageEresed,testSizeProportion,randomSplitState, AlvaDescPath, 
                                                  correlationMethod, correlationLimitValue)
