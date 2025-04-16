# Cache parameters
cache_size = 16 * 1024  # 16KB
block_size = 32         # 32B
associativity = 2

# Calculate the number of sets
num_sets = (cache_size // block_size) // associativity

# Choose a specific set index (e.g., index 0) for simplicity
set_index = 0

# Open the trace file for writing
with open("trace4.txt", "w") as f:
    # Generate two unique addresses that map to the chosen set index
    base_address = set_index * block_size * associativity
    addresses = [base_address, base_address + block_size]
    
    # First 5 accesses - Misses (alternating reads and writes)
    for i in range(5):
        access_type = i % 2  # Alternating between 0 (read) and 1 (write)
        f.write(f"{access_type} {addresses[i % 2]:08x}\n")  # Alternating addresses for misses

    # Next 5 accesses - Hits (same addresses as above)
    for i in range(5):
        access_type = i % 2  # Alternating between 0 (read) and 1 (write)
        f.write(f"{access_type} {addresses[i % 2]:08x}\n")  # Same addresses for hits
