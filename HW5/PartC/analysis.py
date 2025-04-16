import pandas as pd
import matplotlib.pyplot as plt
import sys

if (len(sys.argv)) > 1:
    file_name = sys.argv[1]
else:
    print("Usage: python3 <file name> <csv file name>")
    exit()

# Read the csv file
data = pd.read_csv(file_name)

########################################### ERROR PLOT ###########################################
# Calculate the error (absolute difference between result and actual value)
actual_value = 148.413159
data['Error'] = abs(data['Result'] - actual_value)

# Plot Error vs. Terms for each thread count
plt.figure(figsize=(10, 6))
for thread in data['Threads'].unique():
    subset = data[data['Threads'] == thread]
    plt.plot(subset['Terms'], subset['Error'], marker='o', label=f'{thread} Threads')

plt.xlabel('Number of Terms')
plt.ylabel('Error in Computation')
plt.title('Error in Computation vs. Number of Terms')
plt.legend()
plt.grid(True)
plt.savefig("Figure1.png")
plt.show()

########################################## SPEEDUP PLOT ##########################################
# Extract the base time for single-threaded execution for each number of terms
unique_terms = data['Terms'].unique()
plt.figure(figsize=(10, 6))

# Plot speedup for each unique number of terms
for terms in unique_terms:
    subset = data[data['Terms'] == terms].copy()
    base_time = subset[subset['Threads'] == 1]['Time'].values[0]
    subset['Speedup'] = base_time / subset['Time']  # Calculate speedup
    plt.plot(subset['Threads'], subset['Speedup'], marker='o', label=f'{terms} Terms')

plt.xlabel('Number of Threads')
plt.ylabel('Speedup')
plt.title('Speedup vs Number of Threads')
plt.grid(True)
plt.legend()
plt.savefig("Figure2.png")
plt.show()
