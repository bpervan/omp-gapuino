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
#include "omp_gap8.h"
typedef struct L1_structure0{
int a;
int c;
int b;
int r;
int soma;
int N;
}L1_structure0;
L1_structure0 estrutura0;
void generic_function0(void* gen_var0){
int x_flagsingle_x=0;
L1_structure0 L1_structure;
L1_structure = estrutura0;
int new_n = (L1_structure.N/CORE_NUMBER)*(omp_get_thread_num()+1);
if (omp_get_thread_num()==CORE_NUMBER-1)new_n = new_n+ L1_structure.N%CORE_NUMBER;
int i= 0+(L1_structure.N/CORE_NUMBER)*omp_get_thread_num();
for(i;i<new_n; i++)

    {
EU_MutexLock(0);
{
            estrutura0.a+=L1_structure.b+i;
            estrutura0.c+=estrutura0.a;

EU_MutexUnlock(0);
}
        printf("o valor de i no core %d e: %d\n",omp_get_thread_num(),i);

        L1_structure.soma+=L1_structure.b+estrutura0.c;

        printf("soma = %d no core: %d\n", L1_structure.soma, omp_get_thread_num());

    }
CLUSTER_SynchBarrier();
printf("soma: %d - core %d\n", L1_structure.soma, omp_get_thread_num());
EU_MutexLock(0);


estrutura0.soma=estrutura0.soma+L1_structure.soma;
EU_MutexUnlock(0);

}
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0((void*)x);
}


void Master_Entry(void *arg) {
    CLUSTER_CoresFork(caller, arg);
}
int main()
{
    int soma=0,a=10,w=5,b=10,c=2,r = 30;
    int N = 20;
estrutura0.a=a;

estrutura0.c=c;

estrutura0.b=b;

estrutura0.r=r;

estrutura0.soma=soma;

estrutura0.N = N;

CLUSTER_Start(0, CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
a=estrutura0.a;

c=estrutura0.c;

soma=soma+estrutura0.soma;

    printf("o resultado da soma depois do parallel for1 e: %d\n",soma);
    exit (0);
}
