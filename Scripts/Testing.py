import pandas as pd 

descriptorsDataFrame = pd.read_feather("../Data/ChEMBL_ExtractorData_CHEMBL372_IC50_1000Descriptors.feather")


# Specify the target column for correlation
target_column = 'standard_value'

# Exclude the first column
columns_to_consider = descriptorsDataFrame.columns[1:]  # Skip the first column
subset_df = descriptorsDataFrame[columns_to_consider]

subset_df = descriptorsDataFrame.drop('canonical_smiles', axis = 1)
correlation = subset_df.corr(method = 'pearson')[target_column]


print(subset_df)
print(correlation)
print(descriptorsDataFrame)
