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
import configparser                # Importing the confinguration
import RandomForest                # Importing the macro called "RandomForest.py"

config = configparser.ConfigParser()
config.read('config.ini')
mode = 'DEFAULT'

ChEMBLDataExtractorMacro.ChEMBLExtractData(config[mode]['targetIDChEMBL'], config[mode]['targetProperty'])
dataFile = DataFilterAndPlotsMacro.ChEMBLDataProcessingMacro(config[mode]['targetIDChEMBL'], 
                                                             config[mode]['targetProperty'],
                                                             int(config[mode]['lowerTargetProperty']), 
                                                             int(config[mode]['higherTargetProperty']), 
                                                             float(config[mode]['percentageErased']), 
                                                             float(config[mode]['testSizeProportion']),
                                                             int(config[mode]['randomSplitState']), 
                                                             config[mode]['AlvaDescPath'], 
                                                             config[mode]['correlationMethod'], 
                                                             float(config[mode]['correlationLimitValue']))

RandomForest.RandomForest(dataFile, int(config[mode]['numberOfTrees']), float(config[mode]['percentageErased']), 
                          float(config[mode]['testSizeProportion']), float(config[mode]['correlationLimitValue']))
