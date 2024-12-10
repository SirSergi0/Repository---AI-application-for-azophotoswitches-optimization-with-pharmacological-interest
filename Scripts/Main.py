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
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
mode = 'DEFAULT'

targetIDChEMBL       = config[mode]['targetIDChEMBL']
targetProperty       = config[mode]['targetProperty']
lowerTargetProperty  = int(config[mode]['lowerTargetProperty'])
higherTargetProperty = int(config[mode]['higherTargetProperty'])
percentageEresed	 = float(config[mode]['percentageErased'])
testSizeProportion	 = float(config[mode]['testSizeProportion'])
randomSplitState     = int(config[mode]['randomSplitState'])

AlvaDescPath		 = config[mode]['AlvaDescPath'] 
correlationMethod    = config[mode]['correlationMethod']
correlationLimitValue= float(config[mode]['correlationLimitValue'])

ChEMBLDataExtractorMacro.ChEMBLExtractData(config[mode]['targetIDChEMBL'], config[mode]['targetProperty'])
DataFilterAndPlotsMacro.ChEMBLDataProcessingMacro(config[mode]['targetIDChEMBL'], config[mode]['targetProperty'],
                                                  int(config[mode]['lowerTargetProperty']), int(config[mode]['higherTargetProperty']), 
                                                  float(config[mode]['percentageErased']), float(config[mode]['testSizeProportion']),
                                                  int(config[mode]['randomSplitState']), config[mode]['AlvaDescPath'], 
                                                  config[mode]['correlationMethod'], float(config[mode]['correlationLimitValue']))
