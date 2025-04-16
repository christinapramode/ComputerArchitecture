import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("pinout_df.csv")

# Plot 1: Comparison of total cache accesses (L1 Instruction, L1 Data, L2, L3)
plt.figure(figsize=(12, 8))
plt.plot(df['O_level'], df['l1_instrn_cache_total_accesses'], label='L1 Instruction Cache Total Accesses', marker='o')
plt.plot(df['O_level'], df['l1_data_cache_total_accesses'], label='L1 Data Cache Total Accesses', marker='x')
plt.plot(df['O_level'], df['l2_cache_total_accesses'], label='L2 Cache Total Accesses', marker='s')
plt.plot(df['O_level'], df['l3_cache_total_accesses'], label='L3 Cache Total Accesses', marker='^')
plt.xlabel('Optimization Level')
plt.ylabel('Total Cache Accesses')
plt.title('Cache Accesses for Different Cache Levels')
plt.legend()
plt.grid(True)
plt.show()

# Plot 2: Total cache miss rates for different cache levels (L1, L2, L3)
plt.figure(figsize=(12, 8))
plt.plot(df['O_level'], df['l1_instrn_cache_total_miss_rate'], label='L1 Instruction Cache Miss Rate', marker='o')
plt.plot(df['O_level'], df['l1_data_cache_total_miss_rate'], label='L1 Data Cache Miss Rate', marker='x')
plt.plot(df['O_level'], df['l2_cache_total_miss_rate'], label='L2 Cache Miss Rate', marker='s')
plt.plot(df['O_level'], df['l3_cache_total_miss_rate'], label='L3 Cache Miss Rate', marker='^')
plt.xlabel('Optimization Level')
plt.ylabel('Miss Rate')
plt.title('Cache Miss Rates for Different Cache Levels')
plt.legend()
plt.grid(True)
plt.show()
