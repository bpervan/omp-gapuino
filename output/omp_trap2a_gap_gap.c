#include "cmsis.h"
#include "gap_common.h"
#include "mbed_wait_api.h"
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <time.h>
#include <stdlib.h>
#define CORE_NUMBER   (4)
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "omp_gap8.h"
/*#define CORE_NUMBER (1)*/
typedef struct L1_structure0{
float global_result;
float a;
float b;
float n;
float qqrcoisa;
}L1_structure0;
L1_structure0 estrutura0;
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
/*------------------------------------------------------------------
 * Function:    f
 * Purpose:     Compute value of function to be integrated
 * Input arg:   x
 * Return val:  f(x)
 */
double f(double x)
{
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
double Local_trap(double a, double b, int n)
{
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
int main()
{
    double  global_result;        /* Store result in global_result */
    double  a=0, b=1000;                 /* Left and right endpoints      */
    int     n=4000;                    /* Total number of trapezoids    */
    int     thread_count=4;
    global_result = 0.0;
    int qqrcoisa = 10;
estrutura0.global_result=global_result;

estrutura0.a=a;

estrutura0.b=b;

estrutura0.n=n;

estrutura0.qqrcoisa=qqrcoisa;

CLUSTER_Start(0,thread_count);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
global_result=estrutura0.global_result;

a=estrutura0.a;

b=estrutura0.b;

n=estrutura0.n;

    printf("With n = %d trapezoids, our estimate\n", n);
    printf("of the integral from %d to %d = %d\n",
            (int) a, (int) b, (int) global_result);
    exit(0);
}  /* main */
void generic_function0(void* gen_var0){
int x_flagsingle_x=0;
        double my_result = 0.0;
        my_result += Local_trap(estrutura0.a, estrutura0.b, estrutura0.n);

EU_MutexLock(0);
        estrutura0.global_result += my_result;
EU_MutexUnlock(0);
    }

