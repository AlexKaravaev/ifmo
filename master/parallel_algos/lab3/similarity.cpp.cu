#include <algorithm>
#include <cassert>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <vector>
#include <chrono>
//#define TEST
#define BLOCKSIZE 16

using std::cout;
using std::generate;
using std::vector;
using namespace std::chrono;

#define gpuErrchk(ans)                        \
    {                                         \
        gpuAssert((ans), __FILE__, __LINE__); \
    }
inline void gpuAssert(cudaError_t code, const char *file, int line, bool abort = true)
{
    if (code != cudaSuccess)
    {
        fprintf(stderr, "GPUassert: %s %s %d\n", cudaGetErrorString(code), file, line);
        if (abort)
            exit(code);
    }
}

__global__ void similarity(const int *A, int *D, int w, int h)
{
    // Compute each thread's global row and column index
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    int temp_sum = 0;
    int diff = 0;

    if ((row < h) && (col < h))
    {
        for (int k = 0; k < w; k++)
        {
            diff = (A[row * w + k] - A[col * w + k]);
            temp_sum += diff * diff;
        }
        D[row * h + col] = temp_sum;
    }
}


__global__ void similarity_shared(const int *A, int *D, int w, int h)
{
    // Compute each thread's global row and column index
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    int tx = threadIdx.x, ty = threadIdx.y;

    int temp_sum = 0;
    int diff = 0;

    __shared__ float as[BLOCKSIZE][BLOCKSIZE];
    __shared__ float as_pow[BLOCKSIZE][BLOCKSIZE];

    if ((row < h) && (col < h))
    {
        for (int k = 0; k < w; k++)
        {
            as[tx][ty] = (A[row * w + k] - A[col * w + k]);
            __syncthreads();
            as_pow[tx][ty] = as[tx][ty]*as[tx][ty];
            __syncthreads();
            temp_sum += as_pow[tx][ty];
            __syncthreads();
        }
        D[row * h + col] = temp_sum;
    }
}

vector<int> similarity_serial(vector<int> A, int w, int h)
{
    vector<int> D;
    for (int row = 0; row < h; row++)
    {
        for (int col = 0; col < h; col++)
        {
            int temp_sum = 0;
            int diff = 0;

            for (int k = 0; k < w; k++)
            {

                diff = (A[row * w + k] - A[col * w + k]);
                temp_sum += diff * diff;
            }
            D.push_back(temp_sum);
        }
    }

    return D;
}

int main()
{

    int w = 32 * 20;
    int h = 32 * 30;

    size_t a_bytes;
    size_t d_bytes;
#ifdef TEST

    w = 3;
    h = 5;
    a_bytes = w * h * sizeof(int);
    d_bytes = h * h * sizeof(int);

#endif
    a_bytes = w * h * sizeof(int);
    d_bytes = h * h * sizeof(int);

    vector<int> A(w * h);
#ifdef TEST

    A[0] = 0;
    A[1] = 1;
    A[2] = 1;
    A[3] = 4;
    A[4] = 0;
    A[5] = 2;
    A[6] = 3;
    A[7] = 1;
    A[8] = 1;
    A[9] = 0;
    A[10] = 0;
    A[11] = 0;
    A[12] = 2;
    A[13] = 1;
    A[14] = 2;
    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < w; j++)
            std::cout << A[i * w + j] << " ";
        std::cout << "\n";
    }
    std::cout << "\n";
#else
    generate(A.begin(), A.end(), []() { return rand() % 100; });

#endif
    vector<int> D(h * h);

    int *d_a, *d_d;
    gpuErrchk(cudaMalloc(&d_a, a_bytes));
    gpuErrchk(cudaMalloc(&d_d, d_bytes));

    gpuErrchk(cudaMemcpy(d_a, A.data(), a_bytes, cudaMemcpyHostToDevice));
    gpuErrchk(cudaMemcpy(d_d, D.data(), d_bytes, cudaMemcpyHostToDevice));

#ifdef TEST
    int THREADS = w;
    int BLOCKS  = h * w / THREADS;
#else
    int THREADS = 16;
    int BLOCKS = BLOCKSIZE;
#endif

    dim3 threads(THREADS, THREADS);
    dim3 blocks(BLOCKS, BLOCKS);

    auto start = high_resolution_clock::now();
    similarity<<<blocks, threads>>>(d_a, d_d, w, h);
    auto stop = high_resolution_clock::now();

    auto duration = duration_cast<nanoseconds>(stop - start);

    gpuErrchk(cudaMemcpy(D.data(), d_d, d_bytes, cudaMemcpyDeviceToHost));

    cout << "CUDA COMPLETED SUCCESSFULLY in " << duration.count() << " nanoseconds \n";
#ifdef TEST
    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < h; j++)
            std::cout << D[i * h + j] << " ";
        std::cout << "\n";
    }

    std::cout << "\n";
#endif

    start = high_resolution_clock::now();
    similarity_shared<<<blocks, threads>>>(d_a, d_d, w, h);
    stop = high_resolution_clock::now();

    duration = duration_cast<nanoseconds>(stop - start);
    
    gpuErrchk(cudaMemcpy(D.data(), d_d, d_bytes, cudaMemcpyDeviceToHost));

    cout << "CUDA SHARED COMPLETED SUCCESSFULLY in " << duration.count() << " nanoseconds \n";
#ifdef TEST
    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < h; j++)
            std::cout << D[i * h + j] << " ";
        std::cout << "\n";
    }

    std::cout << "\n";
#endif


    start = high_resolution_clock::now();
    auto serial = similarity_serial(A, w, h);
    stop = high_resolution_clock::now();
    duration = duration_cast<nanoseconds>(stop - start);
    cout << "SERIAL COMPLETED SUCCESSFULLY in " << duration.count() << " nanoseconds \n";

#ifdef TEST
    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < h; j++)
            std::cout << serial[i * h + j] << " ";
        std::cout << "\n";
    }
#endif
    gpuErrchk(cudaFree(d_a));
    gpuErrchk(cudaFree(d_d));

    cudaPeekAtLastError();
    cudaDeviceSynchronize();
    return 0;
}