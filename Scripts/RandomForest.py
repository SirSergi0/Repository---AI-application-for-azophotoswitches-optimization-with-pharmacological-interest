########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     02/12/2024                                                                                #
#  Purpose:  Implementing the "Random forest" algorithm in order to predict standard values            #
#                                                                                                      #
########################################################################################################

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Importing the desired files
TrainingDataFrame = pd.read_feather("../data/ChEMBL_ExtractorData_CHEMBL372_IC50_1000min_-1max_200FilteredGap_min_17Gap_max_47Train.feather")
TestingDataFrame  = pd.read_feather("../data/ChEMBL_ExtractorData_CHEMBL372_IC50_1000min_-1max_200FilteredGap_min_17Gap_max_47Test.feather")

# adapting the data to the "RandomForest" format
ChemDescriptorsTraining     = TrainingDataFrame.drop(['standard_value','canonical_smiles'], axis=1)
InhibitionPotentialTraining = TrainingDataFrame['standard_value']
ChemDescriptorsTesting      = TestingDataFrame.drop(['standard_value','canonical_smiles'], axis=1)
InhibitionPotentialTesting  = TestingDataFrame['standard_value']

numberOfTreesInTheForrest = [50, 100, 200, 500]

for iNumberOfTrees in numberOfTreesInTheForrest:
    RandomForest = RandomForestRegressor(n_estimators=iNumberOfTrees, random_state=42)
    print(f"Using the 'RandomForest' algorithm for fitting the data with {iNumberOfTrees} trees. This may take a while")
    RandomForest.fit(ChemDescriptorsTraining, InhibitionPotentialTraining)
    InhibitionPotentialPredicted = RandomForest.predict(ChemDescriptorsTesting)
    MeanSquaredError = mean_squared_error(InhibitionPotentialTesting, InhibitionPotentialPredicted)
    r2 = r2_score(InhibitionPotentialTesting, InhibitionPotentialPredicted)
    print(f"iNumberOfTrees    : {iNumberOfTrees}")
    print(f"Mean Squared Error: {MeanSquaredError}")
    print(f"R-squared         : {r2}")
