import matplotlib.pyplot as plt
import pandas as pd
import sys

if (len(sys.argv)) > 2:
    file_name_float = sys.argv[1]
    file_name_double = sys.argv[2]
else:
    print("Usage: python3 <file name> <csv file name float> <csv file name double>")
    exit()

# Read the csv file, and take data only for 100,000 terms
data_float = pd.read_csv(file_name_float)
data_double = pd.read_csv(file_name_double)
filtered_data_float = data_float[data_float['Terms'] == 100000]
filtered_data_double = data_double[data_double['Terms'] == 100000]

# Plot time comparison
plt.figure(figsize=(10, 6))
plt.plot(filtered_data_double['Threads'], filtered_data_double['Time'], marker='o', label='Double Precision')
plt.plot(filtered_data_float['Threads'], filtered_data_float['Time'], marker='o', label='Single Precision')
plt.xlabel('Number of Threads')
plt.ylabel('Time (seconds)')
plt.title('Comparison of Execution Time Between Double and Single Precision')
plt.legend()
plt.grid(True)
plt.savefig("Figure1.png")
plt.show()

# Plot result comparison
plt.figure(figsize=(10, 6))
plt.plot(filtered_data_double['Threads'], filtered_data_double['Result'], marker='o', label='Double Precision')
plt.plot(filtered_data_float['Threads'], filtered_data_float['Result'], marker='o', label='Single Precision')
plt.xlabel('Number of Threads')
plt.ylabel('Result')
plt.title('Comparison of Results Between Double and Single Precision')
plt.legend()
plt.grid(True)
plt.savefig("Figure2.png")
plt.show()
