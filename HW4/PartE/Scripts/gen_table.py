import pandas as pd
import re
import os

file_dir = os.path.dirname(os.getcwd()) + "/Outputs/"

# Function to extract data based on patterns and section content
def extract_data(section, prefix):
    patterns = {
        # ITLB fields
        'itlb_load_hits': r"Load Hits:\s+(\d+)",
        'itlb_load_misses': r"Load Misses:\s+(\d+)",
        'itlb_load_accesses': r"Load Accesses:\s+(\d+)",
        'itlb_load_miss_rate': r"Load Miss Rate:\s+([\d.]+)%",
        'itlb_store_hits': r"Store Hits:\s+(\d+)",
        'itlb_store_misses': r"Store Misses:\s+(\d+)",
        'itlb_store_accesses': r"Store Accesses:\s+(\d+)",
        'itlb_store_miss_rate': r"Store Miss Rate:\s+([\w.%]+)", 
        'itlb_total_hits': r"Total Hits:\s+(\d+)",
        'itlb_total_misses': r"Total Misses:\s+(\d+)",
        'itlb_total_accesses': r"Total Accesses:\s+(\d+)",
        'itlb_total_miss_rate': r"Total Miss Rate:\s+([\d.]+)%",

        # DTLB fields
        'dtlb_load_hits': r"Load Hits:\s+(\d+)",
        'dtlb_load_misses': r"Load Misses:\s+(\d+)",
        'dtlb_load_accesses': r"Load Accesses:\s+(\d+)",
        'dtlb_load_miss_rate': r"Load Miss Rate:\s+([\d.]+)%",
        'dtlb_store_hits': r"Store Hits:\s+(\d+)",
        'dtlb_store_misses': r"Store Misses:\s+(\d+)",
        'dtlb_store_accesses': r"Store Accesses:\s+(\d+)",
        'dtlb_store_miss_rate': r"Store Miss Rate:\s+([\w.%]+)", 
        'dtlb_total_hits': r"Total Hits:\s+(\d+)",
        'dtlb_total_misses': r"Total Misses:\s+(\d+)",
        'dtlb_total_accesses': r"Total Accesses:\s+(\d+)",
        'dtlb_total_miss_rate': r"Total Miss Rate:\s+([\d.]+)%",

        # L1 Instruction Cache fields
        'l1_instrn_cache_load_hits': r"Load Hits:\s+(\d+)",
        'l1_instrn_cache_load_misses': r"Load Misses:\s+(\d+)",
        'l1_instrn_cache_load_accesses': r"Load Accesses:\s+(\d+)",
        'l1_instrn_cache_load_miss_rate': r"Load Miss Rate:\s+([\d.]+)%",
        'l1_instrn_cache_store_hits': r"Store Hits:\s+(\d+)",
        'l1_instrn_cache_store_misses': r"Store Misses:\s+(\d+)",
        'l1_instrn_cache_store_accesses': r"Store Accesses:\s+(\d+)",
        'l1_instrn_cache_store_miss_rate': r"Store Miss Rate:\s+([\d.]+)%",
        'l1_instrn_cache_total_hits': r"Total Hits:\s+(\d+)",
        'l1_instrn_cache_total_misses': r"Total Misses:\s+(\d+)",
        'l1_instrn_cache_total_accesses': r"Total Accesses:\s+(\d+)",
        'l1_instrn_cache_total_miss_rate': r"Total Miss Rate:\s+([\d.]+)%",

        # L1 Data Cache fields
        'l1_data_cache_load_hits': r"Load Hits:\s+(\d+)",
        'l1_data_cache_load_misses': r"Load Misses:\s+(\d+)",
        'l1_data_cache_load_accesses': r"Load Accesses:\s+(\d+)",
        'l1_data_cache_load_miss_rate': r"Load Miss Rate:\s+([\d.]+)%",
        'l1_data_cache_store_hits': r"Store Hits:\s+(\d+)",
        'l1_data_cache_store_misses': r"Store Misses:\s+(\d+)",
        'l1_data_cache_store_accesses': r"Store Accesses:\s+(\d+)",
        'l1_data_cache_store_miss_rate': r"Store Miss Rate:\s+([\d.]+)%",
        'l1_data_cache_total_hits': r"Total Hits:\s+(\d+)",
        'l1_data_cache_total_misses': r"Total Misses:\s+(\d+)",
        'l1_data_cache_total_accesses': r"Total Accesses:\s+(\d+)",
        'l1_data_cache_total_miss_rate': r"Total Miss Rate:\s+([\d.]+)%",

        # L2 Unified Cache fields
        'l2_cache_load_hits': r"Load Hits:\s+(\d+)",
        'l2_cache_load_misses': r"Load Misses:\s+(\d+)",
        'l2_cache_load_accesses': r"Load Accesses:\s+(\d+)",
        'l2_cache_load_miss_rate': r"Load Miss Rate:\s+([\d.]+)%",
        'l2_cache_store_hits': r"Store Hits:\s+(\d+)",
        'l2_cache_store_misses': r"Store Misses:\s+(\d+)",
        'l2_cache_store_accesses': r"Store Accesses:\s+(\d+)",
        'l2_cache_store_miss_rate': r"Store Miss Rate:\s+([\d.]+)%",
        'l2_cache_total_hits': r"Total Hits:\s+(\d+)",
        'l2_cache_total_misses': r"Total Misses:\s+(\d+)",
        'l2_cache_total_accesses': r"Total Accesses:\s+(\d+)",
        'l2_cache_total_miss_rate': r"Total Miss Rate:\s+([\d.]+)%",

        # L3 Unified Cache fields
        'l3_cache_load_hits': r"Load Hits:\s+(\d+)",
        'l3_cache_load_misses': r"Load Misses:\s+(\d+)",
        'l3_cache_load_accesses': r"Load Accesses:\s+(\d+)",
        'l3_cache_load_miss_rate': r"Load Miss Rate:\s+([\d.]+)%",
        'l3_cache_store_hits': r"Store Hits:\s+(\d+)",
        'l3_cache_store_misses': r"Store Misses:\s+(\d+)",
        'l3_cache_store_accesses': r"Store Accesses:\s+(\d+)",
        'l3_cache_store_miss_rate': r"Store Miss Rate:\s+([\d.]+)%",
        'l3_cache_total_hits': r"Total Hits:\s+(\d+)",
        'l3_cache_total_misses': r"Total Misses:\s+(\d+)",
        'l3_cache_total_accesses': r"Total Accesses:\s+(\d+)",
        'l3_cache_total_miss_rate': r"Total Miss Rate:\s+([\d.]+)%"
    }

    section_data = {}
    for key, pattern in patterns.items():
        if key.startswith(prefix):
            match = re.search(pattern, section)
            if match:
                value = match.group(1)
                # Handle "nan%" case
                section_data[key] = float(value) if "rate" in key and value != "nan%" else (float('nan') if value == "nan%" else int(value))
    return section_data

# Function to parse file content
def parse(content):
    data = {}
    
    # Split content based on the sections
    sections = re.split(r'\b(DTLB|ITLB|L1 Instruction Cache|L1 Data Cache|L2 Unified Cache|L3 Unified Cache):', content)
    sections_dict = {sections[i]: sections[i + 1] for i in range(1, len(sections), 2)}

    data.update(extract_data(sections_dict.get('ITLB', ''), 'itlb'))
    data.update(extract_data(sections_dict.get('DTLB', ''), 'dtlb'))
    data.update(extract_data(sections_dict.get('L1 Instruction Cache', ''), 'l1_instrn_cache'))
    data.update(extract_data(sections_dict.get('L1 Data Cache', ''), 'l1_data_cache'))
    data.update(extract_data(sections_dict.get('L2 Unified Cache', ''), 'l2_cache'))
    data.update(extract_data(sections_dict.get('L3 Unified Cache', ''), 'l3_cache'))

    return data

# Define configuration parameters
switches = [1, 2, 3]

#Initialize list of different configuration outputs
df_list = pd.DataFrame()

for switch in switches:
    # Parse each output file
    filename = file_dir + f"{switch}_pinout.txt"
    with open(filename, "r") as file:
        file_content = file.read()

        # Parse data and create dataframe
        parsed_data = [parse(file_content)]
        df = pd.DataFrame(parsed_data)
        df['O_level'] = switch
        df = df[['O_level'] + [col for col in df.columns if col not in ['O_level']]]

        df_list = pd.concat([df_list, df])

# Save dataframe to csv
df_list.to_csv("pinout_df.csv")