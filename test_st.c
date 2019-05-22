#include "cmsis.h"
#include "gap_common.h"
#include "mbed_wait_api.h"
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <time.h>
#include <string.h>
#include <stdlib.h>
#define CORE_NUMBER (8)
typedef struct estrutura{
int a;
int b;

}estrutura;

estrutura* st;


typedef struct estrutura2{
int a;
int b;
}estrutura2;

estrutura2* st2;


void *genfun0(void*arg){
    estrutura* gs;
    gs= malloc(sizeof(estrutura));
  //  gs = (estrutura*)arg;
  //  memcpy(st,gs,sizeof(estrutura));
    gs = st;
    printf("estrutura a = %d, estrutura b = %d\n",gs->a*__core_ID(),gs->b);
    return 0;
}
void *genfun1(void*arg)
{
    estrutura2* gs2;
    gs2 = malloc(sizeof(estrutura2));
 //   memcpy(st2,gs2,sizeof(estrutura2));
   // gs2 = (estrutura*)arg;
    gs2=st2;
    printf("estrutura2 a = %d, estrutura2 b = %d\n",gs2->a*__core_ID(),gs2->b);
    return 0;
}
void *caller(void*arg)
{
    int x=(int)arg;
    
    if(x==0)
        return genfun0((void*)arg);
    else if (x==1)
        return genfun1((void*)arg);


}
void *Master_Entry(void*arg)
{
    CLUSTER_CoresFork(caller,(void*)arg);

}


int main()

{

    int a=10,b=20;
    st = malloc(sizeof(estrutura));
    st2 = malloc(sizeof(estrutura2));
    st->a=a;
    printf("bug do seculo: %d",st->a);
    st->b=b;
    st2->a=a*10;
    st2->b=b*10;

    CLUSTER_Start(0,CORE_NUMBER);
  
    CLUSTER_SendTask(0, Master_Entry,(void*)0, 0);
   // CLUSTER_CoresFork(genfun0,(void*)0);
    CLUSTER_Wait(0);
    CLUSTER_Stop(0);
    
    printf("\nintervalo\n");
    
    CLUSTER_Start(0,CORE_NUMBER);
 //   CLUSTER_CoresFork(genfun1,(void*)0);
    CLUSTER_SendTask(0, Master_Entry, (void *)1, 0);
    CLUSTER_Wait(0);
    CLUSTER_Stop(0);
    free(st+1);
    free(st2+2);

    exit(0);
}



