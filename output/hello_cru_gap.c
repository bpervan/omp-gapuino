#include "cmsis.h"
#include "gap_common.h"
#include "mbed_wait_api.h"
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <time.h>
#define CORE_NUMBER   (8)
generic_function0(void*){
   printf("Hello fom core %d",omp_get_thread_num());
}


#include <stdio.h>
#include <omp.h>
#include "omp_gap8.h"

int main()


return 0;

