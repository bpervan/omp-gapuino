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
int soma;
int b;
int r;
int nada;
}L1_structure0;
L1_structure0* estrutura0;
typedef struct L1_structure1{
int a;
int c;
int soma;
int b;
int r;
int nada;
}L1_structure1;
L1_structure1* estrutura1;
void generic_function0(void* gen_var0){

printf("sera que vai dar certo no core: %d\n",omp_get_thread_num());
}
void generic_function1(void* gen_var1){
L1_structure0* L1_structure = malloc(sizeof(L1_structure0));
L1_structure = estrutura0;
printf("\n%d\n",L1_structure->a);
int new_n = (L1_structure->nada/CORE_NUMBER)*(omp_get_thread_num()+1);
for(int i= 0+(L1_structure->nada/CORE_NUMBER)*omp_get_thread_num(); i<new_n;i++)
{

    estrutura0->a+=L1_structure->b+i;
if(omp_get_thread_num()==0)

    {

        estrutura0->c+=estrutura0->a;

    }

//    printf("o valor de a no core %d e: %d\n",omp_get_thread_num(),estrutura0->a);

    estrutura0->soma+=L1_structure->b+estrutura0->c;

}
EU_MutexLock(0);

estrutura0->soma=estrutura0->soma+L1_structure->soma;
EU_MutexUnlock(0);

}
void generic_function2(void* gen_var2){
L1_structure1* L1_structure = malloc(sizeof(L1_structure1));
L1_structure = estrutura1;
printf("\n%d\n",L1_structure->a);
int new_n = (L1_structure->nada/CORE_NUMBER)*(omp_get_thread_num()+1);
for(int i= 0+(L1_structure->nada/CORE_NUMBER)*omp_get_thread_num(); i<new_n;i++)
{

    estrutura1->a+=1;

    estrutura1->soma*=2;

}
EU_MutexLock(0);

estrutura1->soma=estrutura1->soma*L1_structure->soma;
EU_MutexUnlock(0);

}
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0(x);
if(x ==1)return generic_function1(x);
if(x ==2)return generic_function2(x);
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
}

int main()
{
    int soma=0,a=1,b=10,c=2,r = 30;
    int nada = 2000;
//    function();
estrutura0->soma=soma;
estrutura0->a=a;
printf("teste1 \n%d\n",estrutura0->a);

estrutura0->c=c;

estrutura0->soma=soma;

estrutura0->b=b;

estrutura0->r=r;

CLUSTER_Start(0, CORE_NUMBER);

estrutura0=malloc(CORE_NUMBER*sizeof(L1_structure0));

estrutura0->nada = nada;

CLUSTER_SendTask(0, Master_Entry, (void *)1, 0);
CLUSTER_Wait(0);
free(estrutura0);
CLUSTER_Stop(0);
soma=estrutura0->soma;

estrutura1->soma=soma;

estrutura1->a=a;

estrutura1->c=c;

estrutura1->soma=soma;

estrutura1->b=b;

estrutura1->r=r;

CLUSTER_Start(0, CORE_NUMBER);

estrutura1=malloc(CORE_NUMBER*sizeof(L1_structure1));

estrutura1->nada = nada;

CLUSTER_SendTask(0, Master_Entry, (void *)2, 0);
CLUSTER_Wait(0);
free(estrutura1);
CLUSTER_Stop(0);
soma=estrutura1->soma;

function();
    //teste na main
    //outro teste
printf("o resultado da soma e %d\n",soma);
exit (0);

}

//teste dps da main
