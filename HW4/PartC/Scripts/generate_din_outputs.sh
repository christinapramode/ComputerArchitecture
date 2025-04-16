# Run DineroIV simulations for different prefetching configurations
for fetch_switch in 'a' 'm' 't'; do
    for dist_switch in 1 2 4; do
        dineroIV -l1-dsize 2K -l1-dbsize 64 -l1-dfetch ${fetch_switch} -l1-dpfdist ${dist_switch} -informat d < trace > "${fetch_switch}_${dist_switch}_mode.txt"
    done
done

for fetch_switch in 'l' 's'; do
    dineroIV -l1-dsize 2K -l1-dbsize 64 -l1-dfetch ${fetch_switch} -l1-dpfdist 1 -informat d < trace > "${fetch_switch}_1_mode.txt"
done
