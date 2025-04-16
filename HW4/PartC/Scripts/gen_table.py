import pandas as pd
import re
import os

file_dir = os.path.dirname(os.getcwd()) + "/Outputs/"

# Function to parse file content and extract data
def parse(content):
    patterns = {
        'demand_fetches_total': r"Demand Fetches\s+(\d+)",
        'demand_fetches_instrn': r"Demand Fetches\s+\d+\s+(\d+)",
        'demand_fetches_data': r"Demand Fetches\s+\d+\s+\d+\s+(\d+)",
        'demand_fetches_read': r"Demand Fetches\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'demand_fetches_write': r"Demand Fetches\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'demand_fetches_misc': r"Demand Fetches\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'fraction_total': r"Fraction of total\s+([\d.]+)",
        'fraction_instrn': r"Fraction of total\s+[\d.]+\s+([\d.]+)",
        'fraction_data': r"Fraction of total\s+[\d.]+\s+[\d.]+\s+([\d.]+)",
        'fraction_read': r"Fraction of total\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+([\d.]+)",
        'fraction_write': r"Fraction of total\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+([\d.]+)",
        'fraction_misc': r"Fraction of total\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+([\d.]+)",
        'prefetch_fetches_total': r"Prefetch Fetches\s+(\d+)",
        'prefetch_fetches_instrn': r"Prefetch Fetches\s+\d+\s+(\d+)",
        'prefetch_fetches_data': r"Prefetch Fetches\s+\d+\s+\d+\s+(\d+)",
        'prefetch_fetches_read': r"Prefetch Fetches\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'prefetch_fetches_write': r"Prefetch Fetches\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'prefetch_fetches_misc': r"Prefetch Fetches\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'fraction_prefetch': r"Fraction\s+([\d.]+)",
        'demand_misses_total': r"Demand Misses\s+(\d+)",
        'demand_misses_instrn': r"Demand Misses\s+\d+\s+(\d+)",
        'demand_misses_data': r"Demand Misses\s+\d+\s+\d+\s+(\d+)",
        'demand_misses_read': r"Demand Misses\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'demand_misses_write': r"Demand Misses\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'demand_misses_misc': r"Demand Misses\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'demand_miss_rate_total': r"Demand miss rate\s+([\d.]+)",
        'miss_rate_instrn': r"Demand miss rate\s+[\d.]+\s+([\d.]+)",
        'miss_rate_data': r"Demand miss rate\s+[\d.]+\s+[\d.]+\s+([\d.]+)",
        'miss_rate_read': r"Demand miss rate\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+([\d.]+)",
        'miss_rate_write': r"Demand miss rate\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+([\d.]+)",
        'miss_rate_misc': r"Demand miss rate\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+([\d.]+)",
        'prefetch_misses_total': r"Prefetch Misses\s+(\d+)",
        'prefetch_misses_instrn': r"Prefetch Misses\s+\d+\s+(\d+)",
        'prefetch_misses_data': r"Prefetch Misses\s+\d+\s+\d+\s+(\d+)",
        'prefetch_misses_read': r"Prefetch Misses\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'prefetch_misses_write': r"Prefetch Misses\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'prefetch_misses_misc': r"Prefetch Misses\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'pf_miss_rate': r"PF miss rate\s+([\d.]+)",
        'total_misses_total': r"Total Misses\s+(\d+)",
        'total_misses_instrn': r"Total Misses\s+\d+\s+(\d+)",
        'total_misses_data': r"Total Misses\s+\d+\s+\d+\s+(\d+)",
        'total_misses_read': r"Total Misses\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'total_misses_write': r"Total Misses\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'total_misses_misc': r"Total Misses\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'total_miss_rate': r"Total miss rate\s+([\d.]+)",
        'multi_block_refs': r"Multi-block refs\s+(\d+)",
        'bytes_from_memory': r"Bytes From Memory\s+(\d+)",
        'bytes_from_memory_per_demand_fetch': r"\( / Demand Fetches\)\s+([\d.]+)",
        'bytes_to_memory': r"Bytes To Memory\s+(\d+)",
        'bytes_to_memory_per_demand_write': r"\( / Demand Writes\)\s+([\d.]+)",
        'total_bytes_rw_mem': r"Total Bytes r/w Mem\s+(\d+)",
        'total_bytes_rw_mem_per_demand_fetch': r"\( / Demand Fetches\)\s+([\d.]+)"
    }
    
    fields_re = {key: re.compile(pattern) for key, pattern in patterns.items()}

    data = {}
    for key, regex in fields_re.items():
        match = regex.search(content)
        if match:
            data[key] = float(match.group(1)) if "fraction" in key or "rate" in key else int(float(match.group(1)))

    return data

# Define configuration parameters
fetch_switch = ['a', 'm', 't', 'l', 's']

#Initialize list of different configuration outputs
df_list = pd.DataFrame()

for fswitch in fetch_switch:
    # Parse each output file
    if fswitch in ['a', 'm', 't']:
        dist_switch = [1, 2, 4]
    else:
        dist_switch = [1]
    
    for dswitch in dist_switch:
        filename = file_dir + f"{fswitch}_{dswitch}_mode.txt"
        with open(filename, "r") as file:
            file_content = file.read()

            # Parse data and create dataframe
            parsed_data = [parse(file_content)]
            df = pd.DataFrame(parsed_data)
            df['fswitch'] = fswitch
            df['dswitch'] = dswitch
            df = df[['fswitch', 'dswitch'] + [col for col in df.columns if col not in ['fswitch', 'dswitch']]]

            df_list = pd.concat([df_list, df])

# Save dataframe to csv
df_list.to_csv(f"output_table.csv")