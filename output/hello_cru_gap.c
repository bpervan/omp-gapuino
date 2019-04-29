#include "cmsis.h"
#include "gap_common.h"
#include "mbed_wait_api.h"
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <time.h>
#define CORE_NUMBER   (8)
#include <stdio.h>
#include "omp_gap8.h"
typedef struct L1_structure0{
int b
int c
int a
int ricardo_milos
}L1_structure0
void generic_function0(void* gen_var0){

printf("sera que vai dar certo no core: %d\n",omp_get_thread_num());
}
void generic_function1(void* gen_var1){
L1_structure0 L1_structure = (L1_structure0) gen_var1
int new_n = (L1_structure0.n/CORE_NUMBER)*(omp_get_thread_num()+1)
for(L1_structure.i= (n/CORE_NUMBER)*omp_get_thread_num(); L1_structure.i<new_n;L1_structure.i++)
{

for (int i = 0 ; i < n ;  i++  )
}
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0(0);
if(x ==1)return generic_function1(0);
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
    int a,b=10,c=2;
    n = 2000;
L1_structure0 L1_vect0

L1_vect = L1_malloc(CORE_NUMBER*sizeof(L1_structure0)

L1_vect.ricardo_milos=ricardo_milos

CLUSTER_Start(0, CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)1, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
{
    a+=b*i;
    c+=a;
    printf("o valor de a no core %d e: %d\n",a,omp_get_thread_num());
}
printf("Hello fom core %d\n",omp_get_thread_num());
function();
    //teste na main
    //outro teste

exit (0);

}

//teste dps da main
