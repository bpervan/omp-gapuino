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
//#include "omp_gap8.h"
typedef struct L1_structure0{
float global_result;
float a;
float b;
float n;
}L1_structure0;
L1_structure0 estrutura0;
void generic_function0(void* gen_var0){
int x_flagsingle_x=0;
      double my_result = 0.0;
      my_result += Local_trap(L1_structure.a, L1_structure.b, L1_structure.n);

EU_MutexLock(0);
      estrutura0.global_result += my_result;
EU_MutexUnlock(0);
   

}
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0((void*)x);
}


void Master_Entry(void *arg) {
    CLUSTER_CoresFork(caller, arg);
}
double f(double x);    /* Function we're integrating */
double Local_trap(double a, double b, int n);
int main()
{
   double  global_result;        /* Store result in global_result */
   double  a, b;                 /* Left and right endpoints      */
   int     n=800;                    /* Total number of trapezoids    */
   int     thread_count;
   thread_count = 8;
   printf("Enter a, b, and n\n");
   a=0;
   b=10000;
   if (n % thread_count != 0) printf("o codigo funciona para numero de trapezios divisivel por numero de cores\n");
   global_result = 0.0;
estrutura0.global_result=global_result;

estrutura0.a=a;

estrutura0.b=b;

estrutura0.n=n;

CLUSTER_Start(0, CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
global_result=estrutura0.global_result;

   printf("With n = %d trapezoids, our estimate\n", n);
   printf("of the integral from %d to %d multiplyed by 1000=%d \n",(int)a,(int)b,(int)(1000*global_result));
   exit(0);
}
double f(double x)
{
   double return_val;
   return_val = x*x;
   return return_val;
}
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
   for (i = 1; i <= local_n-1; i++)
   {
     x = local_a + i*h;
     my_result += f(x);
   }
   my_result = my_result*h;
   return my_result;
}  /* Trap */
