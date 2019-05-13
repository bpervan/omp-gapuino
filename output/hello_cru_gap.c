#include "cmsis.h"
#include "gap_common.h"
#include "mbed_wait_api.h"
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <time.h>
#define CORE_NUMBER   (8)
CLUSTER_Start(0, CORE_NUMBER);
estrutura0=L1_Malloc(CORE_NUMBER*sizeof(L1_structure0));
#include <stdio.h>
#include "omp_gap8.h"
typedef struct L1_structure0{
int a;
int c;
int soma;
int b;
int ricardo_milos;
int nada;
int i;
}L1_structure0;
L1_structure0* estrutura0;
void generic_function0(void* gen_var0){

printf("sera que vai dar certo no core: %d\n",omp_get_thread_num());
}
void generic_function1(void* gen_var1){
L1_structure0 L1_structure = (L1_structure0) estrutura0;
int new_n = (L1_structure->nada/CORE_NUMBER)*(omp_get_thread_num()+1);
for(int i= 0+(L1_structure->nada/CORE_NUMBER)*omp_get_thread_num(); i<new_n;i++)
{

    estrutura0->a+=L1_structure->b+i;
if(omp_get_thread_num()==0)

    {

        estrutura0->c+=estrutura0->a;

    }

    printf("o valor de a no core %d e: %d\n",omp_get_thread_num(),estrutura0->a);

    estrutura0->soma+=L1_structure->b+estrutura0->c;

}
EU_MutexLock(0);

estrutura0->soma=estrutura0->soma+L1_structure->soma;
EU_MutexUnlock(0);

}
void caller(void* arg){
int x = (L1_structure1)arg;
if(x ==0)return generic_function0(x);
if(x ==1)return generic_function1(x);
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
    int soma=0,a,b=10,c=2,ricardo_milos = 30;
    int nada = 2000;
estrutura0->soma=soma;

estrutura0->a=a;

estrutura0->c=c;

estrutura0->soma=soma;

estrutura0->b=b;

estrutura0->ricardo_milos=ricardo_milos;

int i;

estrutura0->i= i;

estrutura0->nada = nada;

CLUSTER_SendTask(0, Master_Entry, (void *)1, 0);
CLUSTER_Wait(0);
L1_Free(estrutura1, CORE_NUMBER*sizeof(L1_structure0));
CLUSTER_Stop(0);
soma=estrutura0->soma;

function();
    //teste na main
    //outro teste
printf("o resultado da soma e %d\n",soma);
exit (0);

}

//teste dps da main
