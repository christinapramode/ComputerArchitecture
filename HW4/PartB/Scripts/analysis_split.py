import pandas as pd
import matplotlib.pyplot as plt

# Reading from csv file
data = pd.read_csv("out_split.csv")

# Function to plot comparison of different parameters
def plot_comparison(data, parameter, title, ylabel):
    plt.figure(figsize=(10, 6))
    for assoc in data['l1_dassoc'].unique():
        subset = data[data['l1_dassoc'] == assoc]
        plt.plot(subset['l1_dbsize'], subset[parameter], label=f'{assoc}-way Associative')
    
    plt.title(title)
    plt.xlabel("Block Size (Bytes)")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()

plot_comparison(data,'icache_demand_misses_total','Instruction Cache Demand Misses Total vs. Block Size','Instruction Cache Demand Misses Total')
plot_comparison(data,'dcache_demand_misses_total','Data Cache Demand Misses Total vs. Block Size','Data Cache Demand Misses Total')
plot_comparison(data,'icache_bytes_from_memory','Bytes from Memory (Instruction Cache) vs. Block Size','Bytes from Memory (Instruction Cache)')
plot_comparison(data,'dcache_bytes_from_memory','Bytes from Memory (Data Cache) vs. Block Size', 'Bytes from Memory (Data Cache)')
plot_comparison(data,'icache_total_bytes_rw_mem', 'Total Bytes R/W (Instruction Cache) vs. Block Size', 'Total Bytes R/W (Instruction Cache)')
plot_comparison(data,'dcache_total_bytes_rw_mem','Total Bytes R/W (Data Cache) vs. Block Size', 'Total Bytes R/W (Data Cache)')
