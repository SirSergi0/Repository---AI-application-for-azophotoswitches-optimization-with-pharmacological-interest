import pandas as pd
import matplotlib.pyplot as plt

# Example Series: Correlation values between -1 and 1
correlationDataFrame = pd.Series([0.85, -0.75, 0.4, -0.1, 0.3, -0.5, 0.95, -0.95, 0.0])


# ploting the correlation factors histogram
plt.hist(correlationDataFrame, bins=40, color='purple', range = (-1,1), label=f"Number of descriptors {2*4}")
plt.title('Correlation factors of the computed chemical descriptors')
plt.xlabel('Correlation Values')
plt.ylabel('Frequency')
plt.legend()
# Display the plot
plt.savefig('../Plots/CorrelationFactors2.pdf', format = 'pdf')
