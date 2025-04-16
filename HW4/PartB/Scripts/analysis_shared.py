import pandas as pd
import matplotlib.pyplot as plt

# Read from csv file
data = pd.read_csv('out_shared.csv')

fields_to_plot = {
    'Demand Misses': ['demand_misses_total', 'demand_misses_instrn', 'demand_misses_data'],
    'Miss Rates': ['demand_miss_rate_total', 'miss_rate_instrn', 'miss_rate_data'],
    'Memory Bytes': ['bytes_from_memory', 'bytes_to_memory', 'total_bytes_rw_mem']
}

# Define x-axis label
x_labels = [f"{ubsize}B-{uassoc}way" for ubsize, uassoc in zip(data['l1_ubsize'], data['l1_uassoc'])]

# Plots
for title, fields in fields_to_plot.items():
    plt.figure(figsize=(10, 6))
    for field in fields:
        plt.plot(x_labels, data[field], marker='o', label=field)
    plt.title(title)
    plt.xlabel("Cache Configurations (Block Size - Associativity)")
    plt.ylabel("Value")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    
    plt.tight_layout()
    plt.show()
