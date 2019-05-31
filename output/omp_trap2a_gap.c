#include "cmsis.h"
#include "gap_common.h"
#include "mbed_wait_api.h"
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <time.h>
#include <stdlib.h>
#define CORE_NUMBER   (8)
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
typedef struct L1_structure0{
int ignore;
}L1_structure0;
L1_structure0 estrutura0;
typedef struct L1_structure1{
int ignores;
}L1_structure1;
L1_structure1 estrutura1;
int x_flagsingle_x=0;
void generic_function0(void* gen_var0);
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0((void*)x);
}


void Master_Entry(void *arg) {
    CLUSTER_CoresFork(caller, arg);
}
/* File:    omp_trap2a.c
 * Purpose: Estimate definite integral (or area under curve) using trapezoidal
 *          rule.  This version uses a hand-coded reduction after the function
 *          call.
 *
 * Input:   a, b, n
 * Output:  estimate of integral from a to b of f(x)
 *          using n trapezoids.
 *
 * Compile: gcc -g -Wall -fopenmp -o omp_trap2a omp_trap2a.c -lm
 * Usage:   ./omp_trap2a <number of threads>
 *
 * Notes:
 *   1.  The function f(x) is hardwired.
 *   2.  This version assumes that n is evenly divisible by the
 *       number of threads
 * IPP:  Section 5.4 (p. 222)
 */
double f(double x);    /* Function we're integrating */
double Local_trap(double a, double b, int n);
int main() {
    double  global_result;        /* Store result in global_result */
    double  a=0, b=100;                 /* Left and right endpoints      */
    int     n=40;                    /* Total number of trapezoids    */
    int     thread_count=8;
    global_result = 0.0;
CLUSTER_Start(0,thread_count);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
x_flagsingle_x=0;
    printf("With n = %d trapezoids, our estimate\n", n);
    printf("of the integral from %f to %f = %.14e\n",
      a, b, global_result);
    return 0;
}  /* main */
/*------------------------------------------------------------------
 * Function:    f
 * Purpose:     Compute value of function to be integrated
 * Input arg:   x
 * Return val:  f(x)
 */
double f(double x) {
    double return_val;
    return_val = x*x;
    return return_val;
}  /* f */
/*------------------------------------------------------------------
 * Function:    Local_trap
 * Purpose:     Use trapezoidal rule to estimate part of a definite
 *              integral
 * Input args:
 *    a: left endpoint
 *    b: right endpoint
 *    n: number of trapezoids
 * Return val:  estimate of integral from local_a to local_b
 *
 * Note:        return value should be added in to an OpenMP
 *              reduction variable to get estimate of entire
 *              integral
 */
double Local_trap(double a, double b, int n) {
    double  h, x, my_result;
    double  local_a, local_b;
    int  i, local_n;
    int my_rank = omp_get_thread_num();
    int thread_count = omp_get_num_threads();
    h = (b-a)/n;
    local_n = n/thread_count;
    local_a = a + my_rank*local_n*h;
    local_b = local_a + local_n*h;
    my_result = (f(local_a) + f(local_b))/2.0;
    for (i = 1; i <= local_n-1; i++) {
     x = local_a + i*h;
     my_result += f(x);
    }
    my_result = my_result*h;
    return my_result;
}  /* Trap */
void generic_function0(void* gen_var0){
