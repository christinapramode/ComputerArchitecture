# Run DineroIV simulations for 18 configurations
for cache_type in "split" "shared"; do
    for block_size in 8 16 32; do
        for assoc in 1 2 4; do
            # Define trace files for split or shared cache
            if [ "$cache_type" = "split" ]; then
                dineroIV -l1-isize 8K -l1-ibsize ${block_size} -l1-iassoc ${assoc} -l1-dsize 8K -l1-dbsize ${block_size} -l1-dassoc ${assoc} -informat d < trace > "${cache_type}_${block_size}B_${assoc}way.txt"
            
            else
                # Shared cache with a single 16KB space for both instruction and data
                dineroIV -l1-usize 16K -l1-ubsize ${block_size} -l1-uassoc ${assoc} -informat d < trace > "${cache_type}_${block_size}B_${assoc}way.txt"

            fi
        done
    done
done
