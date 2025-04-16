# Cache parameters
cache_size = 2 * 1024  # 2KB
block_size = 64        # 64B

# Calculate number of cache lines
num_lines = cache_size // block_size

# Generate trace file
with open("trace1.txt", "w") as f:
    for i in range(num_lines):
        # Calculate the address for each line
        address = i * block_size

        # Given instruction catch, hence '2':instruction fetch
        f.write(f"2 {address:x}\n")
