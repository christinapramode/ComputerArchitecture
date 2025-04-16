#define _POSIX_C_SOURCE 199309L
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

// Global variables for thread function
int num_terms, num_threads;
double global_sum = 1.0;
double x;
pthread_mutex_t lock; // Mutex for thread-safe operations

// Thread function
void *compute_terms(void *arg)
{
    // Initializing values
    int thread_id = *(int *)arg;
    double local_sum = 0.0;
    double term = 1.0;

    // Computing the start & end limits for the loop
    int start = (num_terms / num_threads) * thread_id;
    int end = (num_terms / num_threads) * (thread_id + 1);
    if (start == 0)
        start++;
    if (thread_id == num_threads - 1)
        end = num_terms; // Last thread handles remaining terms

    for (int i = start; i < end; i++)
    {
        term *= (double)x / i; // Update term for x^i / i!
        local_sum += term;
    }

    // Updating the sum value
    pthread_mutex_lock(&lock);
    global_sum += local_sum;
    pthread_mutex_unlock(&lock);

    return NULL;
}

int main(int argc, char *argv[])
{
    // Taking in x, number of terms & threads from the command line
    if (argc != 4)
    {
        printf("Usage: %s <x value> <num of terms> <num of threads>\n", argv[0]);
        return -1;
    }
    x = atoi(argv[1]);
    num_terms = atoi(argv[2]);
    num_threads = atoi(argv[3]);

    pthread_t threads[num_threads];
    int thread_ids[num_threads];

    // Initializing mutex for thread synchronization
    pthread_mutex_init(&lock, NULL);

    // Starting the clock
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < num_threads; i++)
    {
        thread_ids[i] = i;
        // Creating a new thread
        pthread_create(&threads[i], NULL, compute_terms, &thread_ids[i]);
    }

    // Waiting for all threads to complete execution before continuing
    for (int i = 0; i < num_threads; i++)
    {
        pthread_join(threads[i], NULL);
    }

    // Ending the clock and calculating elapsed time
    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed_time = (end.tv_sec - start.tv_sec) + (double)(end.tv_nsec - start.tv_nsec) / 1000000000.0;

    printf("Computed e^%f \nResult: %f\n", x, global_sum);
    printf("Time taken (sec): %f \n", elapsed_time);

    // Destroying mutex, freeing resources
    pthread_mutex_destroy(&lock);
    return 0;
}
