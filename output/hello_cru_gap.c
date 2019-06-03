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
float soma;
int num_cores;
}L1_structure0;
L1_structure0 romp_global_structure0;
typedef struct L1_structure1{
float soma;
int nada;
float soma;
int num_cores;
}L1_structure1;
L1_structure1 romp_global_structure1;
typedef struct L1_structure2{
float a;
float c;
float soma;
float b;
float r;
float soma;
int nada;
float soma;
int num_cores;
}L1_structure2;
L1_structure2 romp_global_structure2;
typedef struct L1_structure3{
float a;
float c;
float b;
float r;
float soma;
float w;
int num_cores;
}L1_structure3;
L1_structure3 romp_global_structure3;
int x_flagsingle_x=0;
int romp_cores=CORE_NUMBER;
int cores_num[3];
void generic_function0(void* gen_var0);
void generic_function1(void* gen_var1);
void generic_function2(void* gen_var2);
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0((void*)x);
if(x ==1)return generic_function1((void*)x);
if(x ==2)return generic_function2((void*)x);
}


void Master_Entry(void *arg) {
    CLUSTER_CoresFork(caller, arg);
}


void function()

{

    int soma;

    soma = 10;

cores_num[0]=CORE_NUMBER;

romp_cores=CORE_NUMBER;

romp_global_structure0.soma=soma;

romp_global_structure0.soma=soma;

CLUSTER_Start(0,CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
x_flagsingle_x=0;
romp_cores=CORE_NUMBER;
}



int main()

{

    int soma=10,a=10,w=5,b=10,c=2,r = 30;

    int nada = 20;

    function();

cores_num[1]=CORE_NUMBER;

romp_cores=CORE_NUMBER;

romp_global_structure1.soma=soma;

romp_global_structure1.a=a;

romp_global_structure1.c=c;

romp_global_structure1.soma=soma;

romp_global_structure1.b=b;

romp_global_structure1.r=r;

romp_global_structure1.soma=soma;

romp_global_structure1.nada = nada;

CLUSTER_Start(0,CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)1, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
x_flagsingle_x=0;
romp_cores=CORE_NUMBER;
a=romp_global_structure1.a;

c=romp_global_structure1.c;

soma=soma+romp_global_structure1.soma;

    printf("o resultado da soma depois do parallel for1 e: %d\n",soma);

cores_num[2]=CORE_NUMBER;

romp_cores=CORE_NUMBER;

romp_global_structure2.soma=soma;

romp_global_structure2.a=a;

romp_global_structure2.c=c;

romp_global_structure2.b=b;

romp_global_structure2.r=r;

romp_global_structure2.soma=soma;

romp_global_structure2.w=w;

romp_global_structure2.nada = nada;

CLUSTER_Start(0,CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)2, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
x_flagsingle_x=0;
romp_cores=CORE_NUMBER;
a=romp_global_structure2.a;

c=romp_global_structure2.c;

soma=soma*romp_global_structure2.soma;

        //teste na main

        //outro teste



    printf("o resultado da soma depois do parallel for2 e: %d\n",soma);



    exit (0);



}



//teste dps da main

void generic_function0(void* gen_var0){

    printf("sera que vai dar certo no core: %d - L1_structure.soma: %d\n",omp_get_thread_num(),L1_structure.soma);


}

void generic_function1(void* gen_var1){
L1_structure1 L1_structure;
L1_structure = romp_global_structure1;
int new_n = (L1_structure.nada/CORE_NUMBER)*(omp_get_thread_num()+1);
if (omp_get_thread_num()<L1_structure.nada%cores_num[1])new_n++;
int i= 0+(L1_structure.nada/CORE_NUMBER)*omp_get_thread_num();
for(i;i<new_n; i++)

    {

EU_MutexLock(0);
        romp_global_structure1.a+=L1_structure.b+i;

EU_MutexUnlock(0);
EU_MutexLock(0);
if(++x_flagsingle_x==1)
        {   

            romp_global_structure1.c+=romp_global_structure1.a;


        }


EU_MutexUnlock(0);

        printf("o valor de a no core %d e: %d\n",omp_get_thread_num(),romp_global_structure1.a);


        L1_structure.soma+=L1_structure.b+romp_global_structure1.c;





        printf("soma = %d no core: %d\n", L1_structure.soma, omp_get_thread_num());


    }

EU_MutexLock(0);

romp_global_structure1.soma=romp_global_structure1.soma+L1_structure.soma;
EU_MutexUnlock(0);

}

void generic_function2(void* gen_var2){
L1_structure2 L1_structure;
L1_structure = romp_global_structure2;
int new_n = (L1_structure.nada/CORE_NUMBER)*(omp_get_thread_num()+1);
if (omp_get_thread_num()<L1_structure.nada%cores_num[2])new_n++;
int i= 0+(L1_structure.nada/CORE_NUMBER)*omp_get_thread_num();
for(i;i<new_n; i++)

    {

        romp_global_structure2.a+=1;


EU_MutexLock(0);
        L1_structure.soma*=2;

EU_MutexUnlock(0);

        printf("soma = %d no core: %d\n", L1_structure.soma, omp_get_thread_num());


    }

EU_MutexLock(0);

romp_global_structure2.soma=romp_global_structure2.soma*L1_structure.soma;
EU_MutexUnlock(0);

}

