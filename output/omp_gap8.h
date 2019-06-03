#include "gap_common.h"

// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"

int omp_get_thread_num()
{
	return  __core_ID();
}
extern int romp_cores;
int omp_get_num_threads()
{
    return romp_cores;
//#ifdef CORE_NUMBER
//    return CORE_NUMBER;
//#else
//    return 8;
//#endif
}
