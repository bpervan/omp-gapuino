#include "cmsis.h"
#include "gap_common.h"
#include "mbed_wait_api.h"
#include <stdio.h>
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <stdlib.h>
#include <time.h>

int omp_get_thread_num()
{
	return  __core_ID();
}


