// PRINTF
#include "gap_common.h"
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <stdlib.h>

#define CORE_NUMBER      8

void Hello(void *arg) {
    printf("Hello World from cluster core %d!\n", __core_ID());
}

void teste(void *arg)
{
    printf("outra coisa do core %d\n",__core_ID());
}
void caller (void* arg)
{
    int   x = (int) arg;
    if (x ==1)
        return teste(0);
    if (x ==2)
        return Hello(0);

}
void Master_Entry(void *arg) {
    CLUSTER_CoresFork(caller, arg);
}
int main()
{
    printf("Fabric controller code execution for mbed_os Cluster Power On test\n");
    int a = 2;
    /* Cluster Start - Power on */
    CLUSTER_Start(0, CORE_NUMBER);

    /* FC send a task to Cluster */
    CLUSTER_SendTask(0, Master_Entry,(void*)a , 0);

    /* Cluster Stop - Power down */
    CLUSTER_Stop(0);

    /* Check read values */
    int error = 0;

    if (error) printf("Test failed with %d errors\n", error);
    else printf("Test success\n");

    #ifdef JENKINS_TEST_FLAG
    exit(error);
    #else
    return error;
    #endif
}
