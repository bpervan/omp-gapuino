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
   printf("Hello fom core %d",omp_get_thread_num());
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
CLUSTER_SendTask(0, Master_Entry, (void *) NULL, 0);
CLUSTER_Wait(0);

return 0;
}
