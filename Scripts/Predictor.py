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
from tqdm import tqdm 

config   = configparser.ConfigParser()
config.read('config.ini')
mode     = 'DEFAULT'
aDesc    = AlvaDesc(config[mode]['AlvaDescPath'])
fileName = "providedSmiles"
filePath = f"../SmilesFiles/{fileName}.smiles"
outputDataList = []

DataFramePath = f"../SmilesFiles/{fileName}.feather"
if not os.path.exists(DataFramePath):
    raise ValueError(f"The given file does not exist: {filePath}")

importedDataFrame = pd.read_feather(DataFramePath)

smilesList = importedDataFrame['canonical_smiles']

for iSmile in tqdm(smilesList,"Computating molecule's descriptors"):
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


if not os.path.exists(f"../MachineLearningModels/RandomForestChEMBL_ExtractorData_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_1000min_{config[mode]['lowerTargetProperty']}max_{config[mode]['higherTargetProperty']}FilteredGap_min_80Gap_max_80_Trees{config[mode]['numberOfTrees']}.pkl"):
    raise ValueError(f"The given file does not exist: ../MachineLearningModels/RandomForestChEMBL_ExtractorData_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_1000min_{config[mode]['lowerTargetProperty']}max_{config[mode]['higherTargetProperty']}FilteredGap_min_80Gap_max_80_Trees{config[mode]['numberOfTrees']}.pkl")

with open(f"../MachineLearningModels/RandomForestChEMBL_ExtractorData_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_1000min_{config[mode]['lowerTargetProperty']}max_{config[mode]['higherTargetProperty']}FilteredGap_min_80Gap_max_80_Trees{config[mode]['numberOfTrees']}.pkl", 'rb') as MLFile:
    MLModel = pickle.load(MLFile)

predictionsDataFrame = pd.DataFrame({'canonical_smiles' : smilesList ,'Predictions' : MLModel.predict(predictingDataFrame.drop(['canonical_smiles'], axis=1))})
predictionsDataFrame = pd.merge(importedDataFrame,predictionsDataFrame, on = 'canonical_smiles')

print(f"Saving the predictions in: ../Predictions/Predictions_{fileName}_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_min_{config[mode]['lowerTargetProperty']}_max_{config[mode]['higherTargetProperty']}_trees_{config[mode]['numberOfTrees']}.feather")
print(f"Saving the predictions in: ../Predictions/Predictions_{fileName}_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_min_{config[mode]['lowerTargetProperty']}_max_{config[mode]['higherTargetProperty']}_trees_{config[mode]['numberOfTrees']}.csv")

predictionsDataFrame.to_feather(f"../Predictions/Predictions_{fileName}_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_min_{config[mode]['lowerTargetProperty']}_max_{config[mode]['higherTargetProperty']}_trees_{config[mode]['numberOfTrees']}.feather")
predictionsDataFrame.to_csv(f"../Predictions/Predictions_{fileName}_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_min_{config[mode]['lowerTargetProperty']}_max_{config[mode]['higherTargetProperty']}_trees_{config[mode]['numberOfTrees']}.csv", index=False)

predictionsDataFrame.to_csv(f"../Predictions/Predictions_{fileName}_{config[mode]['targetIDChEMBL']}_{config[mode]['targetProperty']}_min_{config[mode]['lowerTargetProperty']}_max_{config[mode]['higherTargetProperty']}_trees_{config[mode]['numberOfTrees']}",index=False)

