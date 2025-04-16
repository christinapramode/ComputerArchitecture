import pandas as pd
import re
import os

file_dir = os.path.dirname(os.getcwd()) + "/Outputs/"

# Functions to parse file content and extract data
def parse_split_cache(content):
    
    # Regex keywords to capture all fields in the dineroIV output file
    patterns = {
        # Configuration fields
        'l1_isize': r"-l1-isize (\d+)",
        'l1_dsize': r"-l1-dsize (\d+)",
        'l1_ibsize': r"-l1-ibsize (\d+)",
        'l1_dbsize': r"-l1-dbsize (\d+)",
        'l1_isbsize': r"-l1-isbsize (\d+)",
        'l1_dsbsize': r"-l1-dsbsize (\d+)",
        'l1_iassoc': r"-l1-iassoc (\d+)",
        'l1_dassoc': r"-l1-dassoc (\d+)",
        
        # Cache statistics fields for l1-icache
        'icache_demand_fetches_total': r"l1-icache.*?Demand Fetches\s+(\d+)", 
        'icache_demand_fetches_instrn': r"l1-icache.*?Demand Fetches\s+\d+\s+(\d+)",
        'icache_demand_fetches_data': r"l1-icache.*?Demand Fetches\s+\d+\s+\d+\s+(\d+)",
        'icache_demand_fetches_read': r"l1-icache.*?Demand Fetches\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'icache_demand_fetches_write': r"l1-icache.*?Demand Fetches\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'icache_fraction_total': r"l1-icache.*?Fraction of total\s+([\d.]+)",
        'icache_fraction_instrn': r"l1-icache.*?Fraction of total\s+[\d.]+\s+([\d.]+)",
        'icache_fraction_data': r"l1-icache.*?Fraction of total\s+[\d.]+\s+[\d.]+\s+([\d.]+)",
        'icache_demand_misses_total': r"l1-icache.*?Demand Misses\s+(\d+)",
        'icache_demand_misses_instrn': r"l1-icache.*?Demand Misses\s+\d+\s+(\d+)",
        'icache_demand_miss_rate_total': r"l1-icache.*?Demand miss rate\s+([\d.]+)",
        'icache_bytes_from_memory': r"l1-icache.*?Bytes From Memory\s+(\d+)",
        'icache_bytes_to_memory': r"l1-icache.*?Bytes To Memory\s+(\d+)",
        'icache_total_bytes_rw_mem': r"l1-icache.*?Total Bytes r/w Mem\s+(\d+)",
        
        # Cache statistics fields for l1-dcache
        'dcache_demand_fetches_total': r"l1-dcache.*?Demand Fetches\s+(\d+)",
        'dcache_demand_fetches_instrn': r"l1-dcache.*?Demand Fetches\s+\d+\s+(\d+)",
        'dcache_demand_fetches_data': r"l1-dcache.*?Demand Fetches\s+\d+\s+\d+\s+(\d+)",
        'dcache_demand_fetches_read': r"l1-dcache.*?Demand Fetches\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'dcache_demand_fetches_write': r"l1-dcache.*?Demand Fetches\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)",
        'dcache_fraction_total': r"l1-dcache.*?Fraction of total\s+([\d.]+)",
        'dcache_fraction_instrn': r"l1-dcache.*?Fraction of total\s+[\d.]+\s+([\d.]+)",
        'dcache_fraction_data': r"l1-dcache.*?Fraction of total\s+[\d.]+\s+[\d.]+\s+([\d.]+)",
        'dcache_demand_misses_total': r"l1-dcache.*?Demand Misses\s+(\d+)",
        'dcache_demand_misses_instrn': r"l1-dcache.*?Demand Misses\s+\d+\s+(\d+)",
        'dcache_demand_miss_rate_total': r"l1-dcache.*?Demand miss rate\s+([\d.]+)",
        'dcache_bytes_from_memory': r"l1-dcache.*?Bytes From Memory\s+(\d+)",
        'dcache_bytes_to_memory': r"l1-dcache.*?Bytes To Memory\s+(\d+)",
        'dcache_total_bytes_rw_mem': r"l1-dcache.*?Total Bytes r/w Mem\s+(\d+)"
    }

    fields_re = {key: re.compile(pattern, re.DOTALL) for key, pattern in patterns.items()}
    
    data = {}
    for key, regex in fields_re.items():
        match = regex.search(content)
        if match:
            data[key] = int(match.group(1)) if "fraction" not in key and "rate" not in key else float(match.group(1))
    return data

def parse_shared_cache(content):
    patterns = {
        'l1_usize': r"-l1-usize (\d+)",
        'l1_ubsize': r"-l1-ubsize (\d+)",
        'l1_usbsize': r"-l1-usbsize (\d+)",
        'l1_uassoc': r"-l1-uassoc (\d+)",
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
        'bytes_from_memory': r"Bytes From Memory\s+(\d+)",
        'bytes_to_memory': r"Bytes To Memory\s+(\d+)",
        'total_bytes_rw_mem': r"Total Bytes r/w Mem\s+(\d+)"
    }
    
    fields_re = {key: re.compile(pattern) for key, pattern in patterns.items()}

    data = {}
    for key, regex in fields_re.items():
        match = regex.search(content)
        if match:
            data[key] = int(match.group(1)) if "fraction" not in key and "rate" not in key else float(match.group(1))
    return data

# Define configuration parameters
block_sizes = [8, 16, 32]
associativities = [1, 2, 4]
cache_types = ['split', 'shared']

for ctype in cache_types:
    #Initialize list of different configuration outputs
    df_list = pd.DataFrame()

    # Parse each output file
    for block_size in block_sizes:
        for assoc in associativities:
            filename = file_dir + f"{ctype}_{block_size}B_{assoc}way.txt"

            with open(filename, "r") as file:
                file_content = file.read()

                # Parse data and create dataframe
                if (ctype == 'split'):
                    parsed_data = [parse_split_cache(file_content)]
                elif (ctype == 'shared'):
                    parsed_data = [parse_shared_cache(file_content)]

                df = pd.DataFrame(parsed_data)
                df_list = pd.concat([df_list, df])

    # Save dataframe to csv
    df_list.to_csv(f"out_{ctype}.csv")
