# Parameters
num_blocks = 1024  
additional_blocks = 256  # Extra blocks to exceed cache size and cause evictions
block_size = 32

with open("trace5_1.txt", "w") as file:
    # Generate addresses that touch each set, then wrap around to create additional blocks
    for tag_offset in range(2):
        for index in range(additional_blocks):
            address = (tag_offset << 12) | (index * block_size)
            file.write(f"2 {address:08X}\n")
