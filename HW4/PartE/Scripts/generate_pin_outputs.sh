# Run pin outputs for different compiler optimization switches
for fetch_switch in 1 2 3; do
    gcc -o gauss${fetch_switch} -O${fetch_switch} gaussian_elimination.c
    pin -t allcache.so -- ./gauss${fetch_switch} > ${fetch_switch}_pinout.txt 2>&1
done