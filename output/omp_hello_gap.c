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

#include "omp_gap8.h"

typedef struct L1_structure0{
int num_cores;
}L1_structure0;
L1_structure0 romp_global_structure0;
typedef struct L1_structure1{
int num_cores;
}L1_structure1;
L1_structure1 romp_global_structure1;
int x_flagsingle_x=0;
int romp_cores=CORE_NUMBER;
int cores_num[1];
void generic_function0(void* gen_var0);
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0((void*)x);
}


void Master_Entry(void *arg) {
    CLUSTER_CoresFork(caller, arg);
}




void Hello(void);  

int main() {

   int thread_count = 7; 



cores_num[0]=thread_count;

romp_cores=thread_count;

CLUSTER_Start(0,thread_count);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
x_flagsingle_x=0;
romp_cores=CORE_NUMBER;
   exit (0); 

}



void Hello(void) {

   int my_rank = omp_get_thread_num();

   int thread_count = omp_get_num_threads();



   printf("Hello from thread %d of %d\n", my_rank+1, thread_count);



}  /* Hello */

void generic_function0(void* gen_var0){

   Hello();


}

