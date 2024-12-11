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
def RandomForest(dataFileName, NumberOfTrees, silentMode = False):
    # Importing the data 
    TrainingDataFrame = pd.read_feather(f"{dataFileName}Train.feather")
    TestingDataFrame  = pd.read_feather(f"{dataFileName}Train.feather")
    
    # Creating the prediction dataFrame
    PredictedDataFrame = TestingDataFrame[['canonical_smiles','standard_value']].copy()

    # Adapting the data to the "RandomForest" format
    ChemDescriptorsTraining     = TrainingDataFrame.drop(['standard_value','canonical_smiles'], axis=1)
    InhibitionPotentialTraining = TrainingDataFrame['standard_value']
    ChemDescriptorsTesting      = TestingDataFrame.drop(['standard_value','canonical_smiles'], axis=1)
    InhibitionPotentialTesting  = TestingDataFrame['standard_value']
    
    # Generating the Random Forest object
    RandomForest = RandomForestRegressor(n_estimators=NumberOfTrees, random_state=42)
    if not silentMode: print(f"\nUsing the 'RandomForest' algorithm for fitting the data with {NumberOfTrees} trees. This may take a while")

    # Training the Algorithm 
    RandomForest.fit(ChemDescriptorsTraining, InhibitionPotentialTraining)

    # Predicting the inhibitionValues
    InhibitionPotentialPredicted = RandomForest.predict(ChemDescriptorsTesting)
    
    # Adding the results to the 'PredictedDataFrame'
    PredictedDataFrame["PredictedValues"] = InhibitionPotentialPredicted

    # Printing some results data
    if not silentMode: print(f"iNumberOfTrees    : {NumberOfTrees}")
    if not silentMode: print(f"Mean Squared Error: {mean_squared_error(InhibitionPotentialTesting, InhibitionPotentialPredicted)}")
    if not silentMode: print(f"R-squared         : {r2_score(InhibitionPotentialTesting, InhibitionPotentialPredicted)}")
    
    # Saving the PredictedDataFrame into the 'Predictions' directory 
    if not silentMode: print(f"Saving the prediction values into the ../Predictions/{dataFileName.removeprefix("../Data/")}RandomForest.feather file")
    if not silentMode: print(f"Saving the prediction values into the ../Predictions/{dataFileName.removeprefix("../Data/")}RandomForest.csv file")
    PredictedDataFrame.to_feather(f"../Predictions/{dataFileName.removeprefix("../Data/")}RandomForest.feather")
    PredictedDataFrame.to_csv(f"../Predictions/{dataFileName.removeprefix("../Data/")}RandomForest.csv", index=False)
