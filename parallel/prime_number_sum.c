#include <stdio.h>
#include <omp.h>
#include <stdlib.h>

#define TWOTO31 2147483647


int is_prime(long num) {
    if(num == 2) return 1;
    if((num/2) * 2 == num) return 0;
    long i = 0;
    for(i = 3; i < num; i+= 2) {
        if((num/i) * i == num) return 0;
    }
    return 1;
}

int main(int argc, char *argv[]) {
    long sum = 0; // We start with two to avoid considering any pairs
    long limit = 0;
    long i = 3;
    int threads = 1;
    fprintf(stderr,"Usage: ./prime_number_sum MAX_NUM threads\n");
    if(argc > 1) limit = strtoll(argv[1],NULL,10);
    else limit = TWOTO31;
    if(argc > 2) threads = strtoll(argv[2],NULL,10);
    omp_set_dynamic(0);
    omp_set_num_threads(threads);
    printf("Limit: %ld\n",limit);
#pragma omp parallel for reduction(+:sum)
    for(i = 3; i <= limit; i+= 2) {
        if(i == 3) printf("%d\n",omp_get_num_threads());
        if(is_prime(i)) sum = sum + i;
    }
    sum += 2;
    printf("%ld\n",sum);
    return (int)sum;
}
