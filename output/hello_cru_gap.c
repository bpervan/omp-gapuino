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
int nada;
}L1_structure0;
L1_structure0* estrutura0;
typedef struct L1_structure1{
int a;
int c;
int b;
int r;
int soma;
}L1_structure1;
L1_structure1* estrutura1;
typedef struct L1_structure2{
int a;
int c;
int b;
int r;
int soma;
int w;
int nada;
}L1_structure2;
L1_structure2* estrutura2;
void generic_function0(void* gen_var0){
int x_flagsingle_x=0;

printf("sera que vai dar certo no core: %d\n",omp_get_thread_num());
}
void generic_function1(void* gen_var1){
int x_flagsingle_x=0;
L1_structure1* L1_structure = malloc(sizeof(L1_structure1));
L1_structure = estrutura1;
int new_n = (L1_structure->nada/CORE_NUMBER)*(omp_get_thread_num()+1);
for(int i= 0+(L1_structure->nada/CORE_NUMBER)*omp_get_thread_num(); i<new_n;i++)
{
EU_MutexLock(0);

    estrutura2->a+=L1_structure->b+i;
EU_MutexUnlock(0);
if(++x_flagsingle_x==1)

    {
EU_MutexLock(0);

        estrutura2->c+=estrutura2->a;
EU_MutexUnlock(0);

    }
EU_MutexLock(0);

    printf("o valor de a no core %d e: %d\n",omp_get_thread_num(),estrutura2->a);
EU_MutexUnlock(0);
EU_MutexLock(0);

    L1_structure->soma+=L1_structure->b+estrutura2->c;
EU_MutexUnlock(0);

}
EU_MutexLock(0);

estrutura2->soma=estrutura2->soma+L1_structure->soma;
EU_MutexUnlock(0);

}
void generic_function2(void* gen_var2){
int x_flagsingle_x=0;
L1_structure3* L1_structure = malloc(sizeof(L1_structure3));
L1_structure = estrutura3;
int new_n = (L1_structure->nada/CORE_NUMBER)*(omp_get_thread_num()+1);
for(int i= 0+(L1_structure->nada/CORE_NUMBER)*omp_get_thread_num(); i<new_n;i++)
{

    int L1_structure->w
EU_MutexLock(0);

    estrutura4->a+=1;
EU_MutexUnlock(0);

    L1_structure->soma*=2;

}
EU_MutexLock(0);

estrutura4->soma=estrutura4->soma*L1_structure->soma;
EU_MutexUnlock(0);

}
void generic_function3(void* gen_var3){
