# Cache parameters
cache_size = 2 * 1024  # 2KB
block_size = 64        # 64B
associativity = 8

# Calculate number of sets
num_sets = (cache_size // block_size) // associativity

# Open the trace file for writing
with open("trace2.txt", "w") as f:
    for set_index in range(num_sets):
        # Generate three unique addresses per index (set) by using an offset
        base_address = set_index * block_size * associativity
        addresses = [base_address, base_address + block_size, base_address + 2 * block_size]
        
        # Write addresses to file to produce 3 misses and 4 hits
        # Misses
        f.write(f"2 {addresses[0]:x}\n")  # First access to address 1 (miss)
        f.write(f"2 {addresses[1]:x}\n")  # First access to address 2 (miss)
        f.write(f"2 {addresses[2]:x}\n")  # First access to address 3 (miss)

        # Hits
        f.write(f"2 {addresses[0]:x}\n")  # Second access to address 1 (hit)
        f.write(f"2 {addresses[1]:x}\n")  # Second access to address 2 (hit)
        f.write(f"2 {addresses[2]:x}\n")  # Second access to address 3 (hit)
        f.write(f"2 {addresses[0]:x}\n")  # Third access to address 1 (hit)
