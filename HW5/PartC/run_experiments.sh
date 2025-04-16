#!/bin/bash

# Output CSV file
output_file="results.csv"

# Initialize the CSV file with headers
echo "Terms,Threads,Result,Time" > "$output_file"

# Input values
x_value=5
terms_list=(100000 250000 500000 750000)
threads_list=(1 2 4 8 16 32)

# Run the program for each combination of terms and threads
for terms in "${terms_list[@]}"; do
    for threads in "${threads_list[@]}"; do
        output=$(./euler "$x_value" "$terms" "$threads")

        # Extract the result and time from the program's output
        result=$(echo "$output" | grep "Result:" | awk '{print $2}')
        time_taken=$(echo "$output" | grep "Time taken" | awk '{print $4}')

        # Append the data to the CSV file
        echo "$terms,$threads,$result,$time_taken" >> "$output_file"
    done
done

echo "Experiment results saved to $output_file"
