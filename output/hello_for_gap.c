#include "gap_common.h"
#include "gap_cluster.h"
#define CORE_NUMBER   (8)
#include <stdio.h>

#include "omp_gap8.h"

typedef struct L1_structure0{
float a;
float c;
float b;
float r;
float soma;
int N;
int num_cores;
}L1_structure0;
L1_structure0 romp_global_structure0;
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


int main()

{

    int soma=0,a=10,w=5,b=10,c=2,r = 30;

    int N = 20;



cores_num[0]=CORE_NUMBER;

romp_cores=CORE_NUMBER;

romp_global_structure0.soma=soma;

romp_global_structure0.a=a;

romp_global_structure0.c=c;

romp_global_structure0.b=b;

romp_global_structure0.r=r;

romp_global_structure0.soma=soma;

romp_global_structure0.N = N;

CLUSTER_Start(0,CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
x_flagsingle_x=0;
romp_cores=CORE_NUMBER;
a=romp_global_structure0.a;

c=romp_global_structure0.c;

soma=soma+romp_global_structure0.soma;

    exit (0);

}

void generic_function0(void* gen_var0){
L1_structure0 L1_structure;
L1_structure = romp_global_structure0;
int new_n = (L1_structure.N/CORE_NUMBER)*(omp_get_thread_num()+1);
if (omp_get_thread_num()<L1_structure.N%cores_num[0])new_n++;
int i= 0+(L1_structure.N/CORE_NUMBER)*omp_get_thread_num();
for(i;i<new_n; i++)

    {

EU_MutexLock(0);
        {

            romp_global_structure0.a+=L1_structure.b+i;


            romp_global_structure0.c+=romp_global_structure0.a;


            L1_structure.soma+=L1_structure.b+romp_global_structure0.c;


        }


EU_MutexUnlock(0);

        printf("o valor de i no core %d e: %d\n",omp_get_thread_num(),i);


        printf("soma = %d no core: %d\n", L1_structure.soma, omp_get_thread_num());


        printf("o resultado da soma depois do parallel for1 e: %d\n",L1_structure.soma);


    }

EU_MutexLock(0);

romp_global_structure0.soma=romp_global_structure0.soma+L1_structure.soma;
EU_MutexUnlock(0);

}

