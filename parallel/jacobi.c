#include <stdio>
#include <stdout>
#include <math>
double tol = 0.000001;
int k = 0;
float ** main_matrix;

double original_funct() {
}
float **get_matrix(int size) {
    float ** matrix = (float **) malloc(sizeof(float*)*size);
    int i = 0;
    for(i = 0; i < size; i++) {
        matrix[i] = (float *)malloc(sizeof(float)*size);
    }
    return matrix;
}
int jacobi() {
  float **matrix = get_matrix(N);
  for(int i = 0; i < N; i++) {
    for(int j = 0; j < N; j++) {
    }
  }
}
