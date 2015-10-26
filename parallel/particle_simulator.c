#include <stdio.h>
#include <omp.h>
#include <stdlib.h>

#define TWOTO31 2147483647


struct particle {
    float x;
    float y;
    float x_vel;
    float y_vel;
    float x_acc;
    float y_acc;
};

struct particle** generate_particles(int n) {
    int i;
    float x, y;
    struct particle **arr = (struct particle **) malloc(sizeof(void *)*n);
    struct particle *p;
    for(i = 0; i < n; i++) {
        p = (struct particle *) malloc(sizeof(struct particle));
        p->x = (float) rand() / (float)(RAND_MAX) * 10;
        p->y = (float) rand() / (float)(RAND_MAX) * 10;
        p->y_acc = 0; p->y_vel = 0;
        p->x_acc = 0; p->x_vel = 0;
        arr[i] = p;
    }
    return arr;
}
int print_particles(int n, struct particle** arr,int id) {
    int i;
    struct particle *p;
    for(i = 0; i < n; i++) {
        p = arr[i];
        printf("%d,%d,%f,%f\n",id,i+1,p->x,p->y);
    }
}
int free_particles(int n, struct particle** arr) {
    int i;
    struct particle *p;
    for(i = 0; i < n; i++) {
        p = arr[i];
        free(p);
    }
    free(arr);
}

float abs_val(float elm) {
    if(elm < 0) elm = -elm;
    return elm;
}

// Calculates the pows-th power of the elm
float power(float elm, int pows) {
    float res = 1;
    int i;
    if(elm < 0) elm = -elm;
    for(i = 0; i < pows; i++) {
        res = res*elm;
    }
    return res;
}

int calculate_acceleration(struct particle* p, int n, struct particle **arr, int dimensions) {
    int i;
    struct particle* neighbor;
    p->x_acc = 0;
    p->y_acc = 0;
    for(i = 0; i < n; i++) {
        neighbor = arr[i];
        if(neighbor == p) continue; // A particle does not affect itself
        if(dimensions == 1) {
            p->x_acc += (neighbor->x - p->x)/power(abs_val(neighbor->x - p->x),3);
        }
        if(dimensions == 2) {
            // Calculate this buddy
            ;
        }
    }
}

int update_vel_position(struct particle* p, float step_sz) {
    p->x_vel += p->x_acc*step_sz;
    p->y_vel += p->y_acc*step_sz;
    p->x += p->x_vel*step_sz;
    p->y += p->y_vel*step_sz;
}

int main(int argc, char *argv[]) {
    struct particle **arr;
    int dimensions = 1;
    float step = 0.1;
    int num_particles = 2;
    int num_iterations = 10;
    int threads = 1;
    if(argc < 4) {
        fprintf(stderr,"Usage ./particle_simulator #of_particles #of_iterations threads [one_dim / two_dim](default: one_dim)\n");
        //return 1;
    } else {
        num_particles = strtoll(argv[1],NULL,10);
        num_iterations = strtoll(argv[2],NULL,10);
        threads = strtoll(argv[3],NULL,10);
    }
    if(argc > 4 && strcmp(argv[4],"two_dim") == 0) dimensions = 2;
   
    arr =  generate_particles(num_particles);
    int i, j;

    //printf("Iteration, ParticleID, ParticleX, ParticleY\n");
    //print_particles(num_particles,arr,0);
    omp_set_num_threads(threads);
    for(i = 1; i <= num_iterations; i++) {
#pragma omp parallel for
        for(j = 0; j < num_particles; j++) {
            calculate_acceleration(arr[j],num_particles,arr,dimensions);
        }
        for(j = 0; j < num_particles; j++) {
            update_vel_position(arr[j],step);
        }
        //print_particles(num_particles,arr,i);
    }
    free_particles(num_particles,arr);
}
