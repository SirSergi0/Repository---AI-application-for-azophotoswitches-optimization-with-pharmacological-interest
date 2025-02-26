########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     25/02/2024                                                                                #
#  Purpose:  Predict the IC_50 value of a given molecule using a previous model and the smiles file    #
#                                                                                                      #
########################################################################################################

import pandas as pd
import os
import configparser
from alvadesccliwrapper.alvadesc import AlvaDesc
import pickle

config   = configparser.ConfigParser()
config.read('config.ini')
mode     = 'DEFAULT'
aDesc    = AlvaDesc(config[mode]['AlvaDescPath'])
fileName = "Benzene"
filePath = f"../SmilesFiles/{fileName}.smiles"
outputDataList = []

if not os.path.exists(filePath):
    raise ValueError(f"The given file does not exist: {filePath}")

with open(filePath, 'r') as smilesFile:
    smilesList = smilesFile.read().splitlines()


for iSmile in smilesList:
    aDesc.set_input_SMILES(iSmile)
    
    if not aDesc.calculate_descriptors("ALL"):
        print('Error: ' + aDesc.get_error())
        pass
    
    outputDescriptors     = aDesc.get_output_descriptors()
    outputValues          = aDesc.get_output()[0]
    descriptorsDictionary = {'canonical_smiles' : iSmile} 
    for iDescriptor in range(len(outputDescriptors)):
        descriptorsDictionary[outputDescriptors[iDescriptor]] = outputValues[iDescriptor]
    outputDataList.append(descriptorsDictionary)

predictingDataFrame = pd.DataFrame(outputDataList)
predictingDataFrame.fillna(0,inplace = True)

if not os.path.exists(f"../Data/ChEMBL_ExtractorData_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_1000Descriptors.feather"):
    raise ValueError(f"The given file does not exist: ../Data/ChEMBL_ExtractorData_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_1000Descriptors.feather")

computedpredictingDataFrame = pd.read_feather(f"../Data/ChEMBL_ExtractorData_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_1000Descriptors.feather")

predictingDataFrame = predictingDataFrame.loc[:, predictingDataFrame.columns.isin(computedpredictingDataFrame.columns)]


if not os.path.exists(f"../MachineLearningModels/RandomForestChEMBL_ExtractorData_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_1000min_{config[mode]['lowerTargetProperty']}max_{config[mode]['higherTargetProperty']}FilteredGap_min_43Gap_max_43_Trees{config[mode]['numberOfTrees']}.pkl"):
    raise ValueError(f"The given file does not exist: ../MachineLearningModels/RandomForestChEMBL_ExtractorData_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_1000min_{config[mode]['lowerTargetProperty']}max_{config[mode]['higherTargetProperty']}FilteredGap_min_43Gap_max_43_Trees{config[mode]['numberOfTrees']}.pkl")

with open(f"../MachineLearningModels/RandomForestChEMBL_ExtractorData_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_1000min_{config[mode]['lowerTargetProperty']}max_{config[mode]['higherTargetProperty']}FilteredGap_min_43Gap_max_43_Trees{config[mode]['numberOfTrees']}.pkl", 'rb') as MLFile:
    MLModel = pickle.load(MLFile)

chemDescriptorsDataFrame = predictingDataFrame.drop(['canonical_smiles'], axis=1)

print(predictingDataFrame)
print(chemDescriptorsDataFrame)

InhibitionPotentialPredicted = MLModel.predict(chemDescriptorsDataFrame)

print(InhibitionPotentialPredicted)
