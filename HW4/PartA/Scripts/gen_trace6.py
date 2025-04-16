# Parameters
test_set_index = 0          
block_size = 32             
associativity = 4          
extra_addresses = 2         # Extra addresses to exceed associativity and trigger eviction

with open("trace6.txt", "w") as file:
    # Fill the cache set
    for tag_offset in range(associativity):
        address = (tag_offset << 12) | (test_set_index * block_size)
        file.write(f"2 {address:08X}\n")
    
    # Access additional addresses that map to the same set to cause eviction
    for extra_offset in range(extra_addresses):
        # Each new tag will cause an eviction once the set is full
        address = ((associativity + extra_offset) << 12) | (test_set_index * block_size)
        file.write(f"2 {address:08X}\n")
    
    # Re-access the initial addresses to check which ones remain in the cache
    for tag_offset in range(associativity):
        address = (tag_offset << 12) | (test_set_index * block_size)
        file.write(f"2 {address:08X}\n")
