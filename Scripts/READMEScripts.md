# Scripts functionalities
## config.ini
File that contains all the variables of the code, must be changed to fit the porpuses.

## Main.py
It links all the files and store the hole Machine Learning Process. This will be the main script file containing the following scripts

### ChEMBLDataExtractorMacro.py
Import all molecule's data with a known IC50 activity respect a certain protein (i.e, COX-2) from the ChEMBL database. This info will be stored into the `Data` directory.

### DataFilterAndPlotsMacro.py
Analyse the extracted data by ChEMBLDataExtractorMacro.py in order to filter out irrellevant entries, then generating the Training and Testing sets for our Machine Learning Model and plotting the data in the `Plots` directory.

### SlpitAndPrintDataFrameMacro.py
Spliting data frames evenly and printing their rellevant information.

### ComputeChemicalDescriptorsMacro.py
Computing and extracting all the chemical descriptors using AlvaDesc software.

## Predictor.py
Generates predictions using the presets defined in the `config.ini` file, based on the SMILES files stored in the `../SmilesFiles/` directory.

## ProvidedSmiles.py
Stores azophotoswitch data in a Python dictionary for easy access and manipulation.

## plotAzophotoSwitches.py
Responsible for generating plots, which are saved in the `../Plots/` directory.
