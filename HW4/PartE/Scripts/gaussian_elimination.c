#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define N 20

void gaussianElimination(double A[N][N], double b[N])
{
    int i, j, k;

    // Forward elimination
    for (i = 0; i < N - 1; i++)
    {
        for (j = i + 1; j < N; j++)
        {
            double factor = A[j][i] / A[i][i];
            for (k = i; k < N; k++)
            {
                A[j][k] -= factor * A[i][k];
            }
            b[j] -= factor * b[i];
        }
    }

    // Backward substitution
    for (i = N - 1; i >= 0; i--)
    {
        double sum = 0.0;
        for (j = i + 1; j < N; j++)
        {
            sum += A[i][j] * b[j];
        }
        b[i] = (b[i] - sum) / A[i][i];
    }
}

int main()
{
    double A[N][N], b[N];
    int i, j;
    clock_t start, end;

    srand(time(NULL));

    // Generate random numbers between -50 and 50 for the matrix
    for (i = 0; i < N; i++)
    {
        for (j = 0; j < N; j++)
        {
            A[i][j] = (double)rand() / RAND_MAX * 100.0 - 50.0;
        }
        b[i] = (double)rand() / RAND_MAX * 100.0 - 50.0;
    }

    // Start the timer
    start = clock();

    gaussianElimination(A, b);

    // End the timer
    end = clock();

    // Calculate and print the elapsed time
    double elapsed_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Elapsed time: %f seconds\n", elapsed_time);

    return 0;
}