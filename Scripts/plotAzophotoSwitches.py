########################################################################################################
#                                                                                                      #
#  Project:  AI Application for Azophotoswitches Optimization with Pharmacological Interest            #
#  Author:   Sergio Castañeiras Morales                                                                #
#  Date:     27/04/2024                                                                                #
#  Purpose:  Plot main results for the Azophotoswitches                                                #
#                                                                                                      #
########################################################################################################

import pandas as pd
import matplotlib.pyplot as plt

Prediction = pd.read_csv("../Predictions/MainPredictions.csv")
Prediction = Prediction.drop('Unnamed: 8', axis=1)

for i in range(7):
    Prediction = Prediction.drop(52-i, axis=0)

plt.figure(figsize=(10, 7))
plt.scatter(Prediction['Gbinding'],Prediction['Predictions'], color = 'purple')
plt.xlabel('$\Delta G_{binding}$ (Kcal/mol)')
plt.ylabel('Predicted $IC_{50}$ (nM)')
# plt.xlim(-12,12)
# plt.ylim(80,320)
# plt.show()
plt.savefig("../Plots/GbindingVSIC50.pdf")
plt.close()
