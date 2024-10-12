########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     12/10/2024                                                                                #
#  Purpose:  Macro used for spliting data frames evenly and printing their rellevant information       #
#                                                                                                      #
########################################################################################################

import pandas as pd # Importing pandas in order to use DataFrames
import matplotlib.pyplot as plt # Importing matplotlib for perfoming plots
from sklearn.model_selection import train_test_split # Importing the funtion "train_test_split" for spliting our data in two 
# sets. The training set and the testing set.

# Helper function to split the dataframe iteratively
def splitDataFrameIteration(dataFrame, column, splitValue):
    upperCounter = 0; underCounter = 0
    for iData in dataFrame[column]:
        if iData >= splitValue:
            upperCounter += 1
        if iData <= splitValue:
            underCounter += 1
    return underCounter, upperCounter

# Helper function to find split values for data gaps
def findSplitDataFrame(dataFrame, column, percentageEresed):
    iSplitValueUnder = 0
    while True:
        if splitDataFrameIteration(dataFrame, column, iSplitValueUnder)[0] < len(dataFrame) * (1 - percentageEresed) / 2:
            iSplitValueUnder += 1
        else:
            break

    iSplitValueUpper = iSplitValueUnder
    while True:
        if splitDataFrameIteration(dataFrame, column, iSplitValueUpper)[0] < len(dataFrame) * (1 + percentageEresed) / 2:
            iSplitValueUpper += 1
        else:
            break

    return iSplitValueUnder, iSplitValueUpper

def printDataFrameLenMaxMin(dataFrame, targetProperty, standardValue = 'standard_value', standardUnits = 'standard_units', silentMode = False):
    if silentMode != True: print(f'Number of entries:                  {len(dataFrame)}')
    minimum = dataFrame[standardValue].idxmin()
    maximum = dataFrame[standardValue].idxmax()
    if silentMode != True: print(f'Minimum {targetProperty}:                       {float(dataFrame.loc[minimum,standardValue])} {dataFrame.loc[minimum, standardUnits]}')
    if silentMode != True: print(f'Maximum {targetProperty}:                       {float(dataFrame.loc[maximum,standardValue])} {dataFrame.loc[maximum, standardUnits]}\n')
