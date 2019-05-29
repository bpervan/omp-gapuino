#include <stdlib.h>
#include <math.h>
#include "omp_gap8.h" 
//#include "lib/pin.h"


int main() {
    int n, i;
    int thread_count;
    double factor;
    double sum = 0.0;
    int o=0;
    thread_count = 8;
    n = 1000000;

//    PinName trigger = GPIO_A17;

 //   init_pin(trigger);

    /* Set trigger */
  //  set_pin(trigger,1);

#pragma omp parallel for default(none) num_threads(thread_count) private(factor,sum) shared(o) reduction(+:sum) 
    for (i = 0; i < n; i++) 
    {
        factor = (i % 2 == 0) ? 1.0 : -1.0; 
        sum += factor/(2*i+1);
#pragma omp single
        {
            o = omp_get_thread_num(); 
        }

    }

    /* Unset trigger */
   // set_pin(trigger,0);

    sum = 4.0*sum;
    printf("With n = %d terms and %d threads,\n", n, thread_count);
    printf("   Our estimate of pi = %d\n", (int) (100000*sum));
    printf("                   pi = %d\n", (int) (100000*4.0*atan(1.0)));
    printf("o valor de o e: %d\n",o);
    exit (0);
}
