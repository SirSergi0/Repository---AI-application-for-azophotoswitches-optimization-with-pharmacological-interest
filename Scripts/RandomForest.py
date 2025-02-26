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
import pickle
import numpy as np

# Importing the desired files
def RandomForest(dataFileName, NumberOfTrees, percentatgeErased, splitPercentatge, minimumCorrelationFactor, SplitStandardValue, silentMode = False):
    # Importing the data 
    TrainingDataFrame = pd.read_feather(f"{dataFileName}Train.feather")
    TestingDataFrame  = pd.read_feather(f"{dataFileName}Train.feather")
    
    # Creating the prediction dataFrame
    PredictedDataFrame = TestingDataFrame[['canonical_smiles','standard_value']].copy()

    # Adapting the data to the "RandomForest" format
    ChemDescriptorsTraining     = TrainingDataFrame.drop(['standard_value', 'activity_label', 'canonical_smiles'], axis=1)
    InhibitionPotentialTraining = TrainingDataFrame['standard_value']
    ChemDescriptorsTesting      = TestingDataFrame.drop(['standard_value', 'activity_label', 'canonical_smiles'], axis=1)
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
    PredictedDataFrame["activity_label"]  = TestingDataFrame['activity_label']

    # Computing the average 'predicted_activity_label'
    PredictedDataFrame['predicted_activity_label'] = (PredictedDataFrame['PredictedValues'] > SplitStandardValue).astype(int)

    # Analising some statistics
    TruePositive     = ((PredictedDataFrame['activity_label'] == 0) & 
                        (PredictedDataFrame['predicted_activity_label'] == 0)).sum()
    FalsePositive    = ((PredictedDataFrame['activity_label'] == 1) & 
                        (PredictedDataFrame['predicted_activity_label'] == 0)).sum()
    TrueNegative     = ((PredictedDataFrame['activity_label'] == 1) & 
                        (PredictedDataFrame['predicted_activity_label'] == 1)).sum()
    FalseNegative    = ((PredictedDataFrame['activity_label'] == 0) & 
                        (PredictedDataFrame['predicted_activity_label'] == 1)).sum()

    TruePositiveRate = TruePositive/(TruePositive+FalseNegative)
    TrueNegativeRate = TrueNegative/(TrueNegative+FalseNegative)
    ClassificationAcuracy = (TruePositive+TrueNegative)/(TruePositive+FalsePositive+TrueNegative+FalseNegative)
    MatthewsCorrelationFactor = ((TruePositive*TrueNegative)-(FalsePositive*FalseNegative))/(np.sqrt((TruePositive+FalsePositive)*(TruePositive+FalseNegative)*(TrueNegative+FalsePositive)*(TrueNegative+FalseNegative)))


    # Printing some results data
    if not silentMode: print(f"NumberOfTrees            : {NumberOfTrees}")
    if not silentMode: print(f"Erased Percentatge       : {percentatgeErased*100}%")
    if not silentMode: print(f"Splitting proportion     : {splitPercentatge*100}% is for testing")
    if not silentMode: print(f"minimumCorrelationFactor : {minimumCorrelationFactor}")
    if not silentMode: print(f"Number of descriptors    : {ChemDescriptorsTraining.shape[1]}")
    if not silentMode: print(f"Mean Squared Error       : {mean_squared_error(InhibitionPotentialTesting, InhibitionPotentialPredicted)}")
    if not silentMode: print(f"R-squared                : {r2_score(InhibitionPotentialTesting, InhibitionPotentialPredicted)}")
    if not silentMode: print(f"True Positive            : {TruePositive}")
    if not silentMode: print(f"False Positive           : {FalsePositive}")
    if not silentMode: print(f"True Negative            : {TrueNegative}")
    if not silentMode: print(f"False Negative           : {FalseNegative}")
    if not silentMode: print(f"True Positive Rate       : {TruePositiveRate}")
    if not silentMode: print(f"True Negative Rate       : {TrueNegativeRate}")
    if not silentMode: print(f"ClassificationAcuracy    : {ClassificationAcuracy}")
    if not silentMode: print(f"MatthewsCorrelationFactor: {MatthewsCorrelationFactor}")

    # Saving the PredictedDataFrame into the 'Predictions' directory 
    if not silentMode: print(f"Saving the prediction values into the ../Predictions/{dataFileName.removeprefix("../Data/")}RandomForest{NumberOfTrees}.feather file")
    if not silentMode: print(f"Saving the prediction values into the ../Predictions/{dataFileName.removeprefix("../Data/")}RandomForest{NumberOfTrees}.csv file\n")
    PredictedDataFrame.to_feather(f"../Predictions/{dataFileName.removeprefix("../Data/")}RandomForest{NumberOfTrees}.feather")
    PredictedDataFrame.to_csv(f"../Predictions/{dataFileName.removeprefix("../Data/")}RandomForest{NumberOfTrees}.csv", index=False)
    
    # Saving the regression into a binary file using pickle
    with open(f"../MachineLearningModels/RandomForest{dataFileName.removeprefix("../Data/")}_Trees{NumberOfTrees}.pkl", 'wb') as RandomForestFile:
        if not silentMode: print(f"Saving the model into ../MachineLearningModels/RandomForest{dataFileName.removeprefix("../Data/")}_Trees{NumberOfTrees}.pkl")
        pickle.dump(RandomForest, RandomForestFile)

    with open(f"../MachineLearningModels/RandomForestStats{dataFileName.removeprefix("../Data/")}_Trees{NumberOfTrees}.txt", 'w') as RandomForestFile:
        if not silentMode: print(f"Saving the statistics into ../MachineLearningModels/RandomForestStats{dataFileName.removeprefix("../Data/")}_Trees{NumberOfTrees}.txt")
        RandomForestFile.write(f"NumberOfTrees            : {NumberOfTrees}\n")
        RandomForestFile.write(f"Erased Percentatge       : {percentatgeErased*100}%\n")
        RandomForestFile.write(f"Splitting proportion     : {splitPercentatge*100}% is for testing\n")
        RandomForestFile.write(f"minimumCorrelationFactor : {minimumCorrelationFactor}\n")
        RandomForestFile.write(f"Number of descriptors    : {ChemDescriptorsTraining.shape[1]}\n")
        RandomForestFile.write(f"Mean Squared Error       : {mean_squared_error(InhibitionPotentialTesting, InhibitionPotentialPredicted)}\n")
        RandomForestFile.write(f"R-squared                : {r2_score(InhibitionPotentialTesting, InhibitionPotentialPredicted)}\n")
        RandomForestFile.write(f"True Positive            : {TruePositive}\n")
        RandomForestFile.write(f"False Positive           : {FalsePositive}\n")
        RandomForestFile.write(f"True Negative            : {TrueNegative}\n")
        RandomForestFile.write(f"False Negative           : {FalseNegative}\n")
        RandomForestFile.write(f"True Positive Rate       : {TruePositiveRate}\n")
        RandomForestFile.write(f"True Negative Rate       : {TrueNegativeRate}\n")
        RandomForestFile.write(f"ClassificationAcuracy    : {ClassificationAcuracy}\n")
        RandomForestFile.write(f"MatthewsCorrelationFactor: {MatthewsCorrelationFactor}")
