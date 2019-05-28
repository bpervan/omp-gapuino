#include "cmsis.h"
#include "gap_common.h"
#include "mbed_wait_api.h"
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <time.h>
#include <stdlib.h>
#define CORE_NUMBER   (8)
#include <stdlib.h>
#include <math.h>
#include "omp_gap8.h"
#include "lib/pin.h"
typedef struct L1_structure0{
float o;
float factor;
float sum;
int n;
}L1_structure0;
L1_structure0 estrutura0;
void generic_function0(void* gen_var0){
int x_flagsingle_x=0;
L1_structure0 L1_structure;
L1_structure = estrutura0;
int new_n = (L1_structure.n/CORE_NUMBER)*(omp_get_thread_num()+1);
if (omp_get_thread_num()==CORE_NUMBER-1)new_n = new_n+ L1_structure.n%CORE_NUMBER;
int i= 0+(L1_structure.n/CORE_NUMBER)*omp_get_thread_num();
for(i;i<new_n; i++)

    {
        L1_structure.factor = (i % 2 == 0) ? 1.0 : -1.0;

        L1_structure.sum += L1_structure.factor/(2*i+1);
if(++x_flagsingle_x==1)

        {

            estrutura0.o = omp_get_thread_num();

        }

    }
CLUSTER_SynchBarrier();
EU_MutexLock(0);

estrutura0.sum=estrutura0.sum+L1_structure.sum;
EU_MutexUnlock(0);

}
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0((void*)x);
}


void Master_Entry(void *arg) {
    CLUSTER_CoresFork(caller, arg);
}
int main() {
    int n, i;
    int thread_count;
    double factor;
    double sum = 0.0;
    int o=0;
    thread_count = 4;
    n = 1000000;
    PinName trigger = GPIO_A17;
    init_pin(trigger);
    /* Set trigger */
    set_pin(trigger,1);
estrutura0.o=o;

estrutura0.factor=factor;

estrutura0.sum=sum;

estrutura0.n = n;

CLUSTER_Start(0, CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
o=estrutura0.o;

sum=sum+estrutura0.sum;

    /* Unset trigger */
    set_pin(trigger,0);
    sum = 4.0*sum;
    printf("With n = %d terms and %d threads,\n", n, thread_count);
    printf("   Our estimate of pi = %d\n", (int) (100000*sum));
    printf("                   pi = %d\n", (int) (100000*4.0*atan(1.0)));
    printf("o valor de o e: %d\n",o);
    exit (0);
}
