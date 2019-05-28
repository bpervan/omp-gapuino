#include "gap_common.h"

// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"

#define CORE_NUMBER (1)

int omp_get_thread_num()
{
	return  __core_ID();
}

int omp_get_num_threads()
{
    return CORE_NUMBER;
}
