# Scripts functionalities
## Main.py
Link all the files and store the hole Machine Learning Process. This will be the main script file.

## ChEMBLDataExtractorMacro.py
Import all molecule's data with a known IC50 activity respect a certain protein (i.e, COX-2) from the ChEMBL database. This info will be stored into the `Data` directory.

## DataFilterAndPlotsMacro.py
Analyse the extracted data by ChEMBLDataExtractorMacro.py in order to filter out irrellevant entries, then generating the Training and Testing sets for our Machine Learning Model and plotting the data in the `Plots` directory.

## SlpitAndPrintDataFrameMacro.py
Spliting data frames evenly and printing their rellevant information