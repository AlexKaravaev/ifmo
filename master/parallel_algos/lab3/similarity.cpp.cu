#include <algorithm>
#include <cassert>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <vector>

using std::cout;
using std::generate;
using std::vector;



__global__ void similarity(const int* A, int *D, int w, int h){
    // Compute each thread's global row and column index
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    int temp_sum = 0;
    int diff = 0;

    if ((row < h) && (col < h)){
        for (int k = 0; k < w; k++){
            diff = (A[row*w + k] - A[col*w + k]);
            temp_sum += diff*diff;
            printf(
                "row*n+col: %d row*n+k: %d row: %d, col: %d A[%d,%d]: %d"
                " A[%d,%d]: %d sum: %d\n ", 
                row*w + k, col*h + k, row, col, row, col,A[row*w + k],
                row, col, A[col*h + k], diff);
            }
        D[row * h + col] = temp_sum;
    }
}


vector<int> similarity_serial(vector<int> A, int w, int h){
    // Compute each thread's global row and column index

    vector<int> D;
    for (int row = 0; row < h; row++){
        for (int col = 0; col < h; col++)
        {
            int temp_sum = 0;
            int diff = 0;

            for (int k = 0; k < w; k++){
          
                diff = (A[row*w + k] - A[col*w + k]);
                temp_sum += diff*diff;
                printf(
                    "row*n+col: %d row*n+k: %d row: %d, col: %d A[%d,%d]: %d"
                    " A[%d,%d]: %d sum: %d\n", 
                    row*h + k, col*w + k, row, col, row, col, A[row*h + k],
                    row,col, A[col*w + k], diff);
                }
            D.push_back(temp_sum);

        }
    }

    return D;
}
int main() {

    // Define matrix size
    int w = 3;
    int h = 5;

    // Size (in bytes) of matrix
    size_t a_bytes = w * h * sizeof(int);
    size_t d_bytes = h * h * sizeof(int);

    vector<int> A(w * h);
    vector<int> D(h * h);

    // Initialize matrices
    //generate(A.begin(), A.end(), []() { return rand() % 100; });

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

    for (int i=0;i<h;i++){
        for (int j=0;j<w;j++)
            std::cout << A[i*w + j] << " ";
        std::cout << "\n";
    }
     std::cout << "\n";
      // Allocate device memory
      int *d_a, *d_d;
      cudaMalloc(&d_a, a_bytes);
      cudaMalloc(&d_d, d_bytes);

      // Copy data to the device

      cudaMemcpy(d_a, A.data(), a_bytes, cudaMemcpyHostToDevice);
      cudaMemcpy(d_d, D.data(), d_bytes, cudaMemcpyHostToDevice);

      // Threads per CTA dimension
      int THREADS = h;

      // Blocks per grid dimension (assumes THREADS divides N evenly)
      int BLOCKS = h * h / THREADS;

      // Use dim3 structs for block  and grid dimensions
      dim3 threads(THREADS, THREADS);
      dim3 blocks(BLOCKS, BLOCKS);

      // Launch kernel
      similarity<<<blocks, threads>>>(d_a, d_d, w, h);

  // Copy back to the host
  cudaMemcpy(D.data(), d_d, d_bytes, cudaMemcpyDeviceToHost);

  // Check result
  // verify_result(h_a, h_b, h_c, N);

  cout << "COMPLETED SUCCESSFULLY\n";
  for (int i=0;i<h;i++){
      for (int j=0;j<h;j++)
      std::cout << D[i*h + j] << " ";
      std::cout << "\n";
    }

  std::cout << "\n";
  auto serial = similarity_serial(A,w,h);
  for (int i=0;i<h;i++){
      for (int j=0;j<h;j++)
      std::cout << serial[i*h + j] << " ";
      std::cout << "\n";
    }

  // Free memory on device
  cudaFree(d_a);
  cudaFree(d_d);


  return 0;
}