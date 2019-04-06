#include "cmsis.h"
#include "gap_common.h"
#include "mbed_wait_api.h"
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <time.h>
#define CORE_NUMBER   (8)
#include <stdio.h>
#include "omp_gap8.h"
void generic_function0(void* gen_var0){
   printf("Hello fom core %d\n",omp_get_thread_num());
}
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0(0);
}


void Master_Entry(void *arg) {
    CLUSTER_CoresFork(caller, arg);
}
int main()
{
CLUSTER_Start(0, CORE_NUMBER);
int *L1_mem = L1_Malloc(8);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
printf("Waiting...\n");
CLUSTER_Wait(0);
CLUSTER_Stop(0);
exit(0);
}
//teste dps da main
