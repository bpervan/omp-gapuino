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
int ignore;
}L1_structure0;
L1_structure0 estrutura0;
typedef struct L1_structure1{
int a;
int c;
int b;
int r;
int soma;
int nada;
}L1_structure1;
L1_structure1 estrutura1;
typedef struct L1_structure2{
int a;
int c;
int b;
int r;
int soma;
int w;
int nada;
}L1_structure2;
L1_structure2 estrutura2;
void generic_function0(void* gen_var0){
int x_flagsingle_x=0;

printf("sera que vai dar certo no core: %d\n",omp_get_thread_num());
}
void generic_function1(void* gen_var1){
int x_flagsingle_x=0;
L1_structure1 L1_structure;
L1_structure = estrutura1;
int new_n = (L1_structure.nada/CORE_NUMBER)*(omp_get_thread_num()+1);
int i= 0+(L1_structure.nada/CORE_NUMBER)*omp_get_thread_num();
for(i;i<new_n; i++)
{

    estrutura1.a+=L1_structure.b+i;
if(++x_flagsingle_x==1)

    {

        printf("%d\n",estrutura1.a);

        estrutura1.c+=estrutura1.a;

    }

    printf("o valor de a no core %d e: %d\n",omp_get_thread_num(),estrutura1.a);

    L1_structure.soma+=L1_structure.b+estrutura1.c;

    printf("soma = %d no core: %d\n", L1_structure.soma, omp_get_thread_num());

}
CLUSTER_SynchBarrier();
EU_MutexLock(0);

estrutura1.soma=estrutura1.soma+L1_structure.soma;
EU_MutexUnlock(0);

}
void generic_function2(void* gen_var2){
int x_flagsingle_x=0;
L1_structure2 L1_structure;
L1_structure = estrutura2;
int new_n = (L1_structure.nada/CORE_NUMBER)*(omp_get_thread_num()+1);
int i= 0+(L1_structure.nada/CORE_NUMBER)*omp_get_thread_num();
for(i;i<new_n; i++)
{

    estrutura2.a+=1;
EU_MutexLock(0);
    L1_structure.soma*=2;
EU_MutexUnlock(0);

    printf("soma = %d no core: %d\n", L1_structure.soma, omp_get_thread_num());

}
CLUSTER_SynchBarrier();
EU_MutexLock(0);

estrutura2.soma=estrutura2.soma*L1_structure.soma;
EU_MutexUnlock(0);

}
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0((void*)x);
if(x ==1)return generic_function1((void*)x);
if(x ==2)return generic_function2((void*)x);
}


void Master_Entry(void *arg) {
    CLUSTER_CoresFork(caller, arg);
}
void function(){
int soma;
soma = 10;
CLUSTER_Start(0, CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
printf("sera que vai dar certo no core: %d\n",omp_get_thread_num());
}
int main()
{
    int soma=10,a=10,w=5,b=10,c=2,r = 30;
    int nada = 20;
    function();
estrutura1.a=a;

estrutura1.c=c;

estrutura1.b=b;

estrutura1.r=r;

estrutura1.soma=soma;

estrutura1.nada = nada;

CLUSTER_Start(0, CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)1, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
soma=soma+estrutura1.soma;

printf("o resultado da soma depois do parallel for1 e: %d\n",soma);
estrutura2.a=a;

estrutura2.c=c;

estrutura2.b=b;

estrutura2.r=r;

estrutura2.soma=soma;

estrutura2.w=w;

estrutura2.nada = nada;

CLUSTER_Start(0, CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)2, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
soma=soma*estrutura2.soma;

    //teste na main
    //outro teste
printf("o resultado da soma depois do parallel for2 e: %d\n",soma);
exit (0);
}
//teste dps da main
