
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>   
#include "omp_gap8.h"

void Hello(void);  
int main() {
   int thread_count = 7; 

#  pragma omp parallel num_threads(thread_count) 
   Hello();
   exit (0); 
}

void Hello(void) {
   int my_rank = omp_get_thread_num();
   int thread_count = omp_get_num_threads();

   printf("Hello from thread %d of %d\n", my_rank+1, thread_count);

}  /* Hello */
