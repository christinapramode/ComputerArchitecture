# Cache parameters
cache_size = 2 * 1024  # 2KB
block_size = 64        # 64B
associativity = 2      

# Calculate number of sets
num_sets = (cache_size // block_size) // associativity

# Open the trace file for writing
with open("trace3.txt", "w") as f:
    for set_index in range(num_sets):
            # Generate three unique addresses per index (set) by using an offset
            base_address = set_index * block_size * associativity
            addresses = [base_address, base_address + block_size, base_address + 2 * block_size]

            # Pattern: (M, H, M, H, M, H)
            # Access address 1 
            f.write(f"2 {addresses[0]:x}\n")  # Miss
            f.write(f"2 {addresses[0]:x}\n")  # Hit
            
            # Access address 2
            f.write(f"2 {addresses[1]:x}\n")  # Miss
            f.write(f"2 {addresses[1]:x}\n")  # Hit
            
            # Access address 3
            f.write(f"2 {addresses[2]:x}\n")  # Miss
            f.write(f"2 {addresses[2]:x}\n")  # Hit
