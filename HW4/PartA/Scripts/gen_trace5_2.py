# Parameters
associativity_test_set = 0  # Set index to test (e.g., set 0)
block_size = 32  
num_addresses = 16

with open("trace5_2.txt", "w") as file:
    for tag_offset in range(num_addresses):
        address = (tag_offset << 12) | (associativity_test_set * block_size)
        file.write(f"2 {address:08X}\n")
