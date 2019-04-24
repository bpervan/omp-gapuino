#include <stdio.h>
#include <omp.h>
#include "omp_gap8.h"
void function(){
int soma;
soma = 10;
#pragma omp parallel
printf("sera que vai dar certo no core: %d\n",omp_get_thread_num());
}

int main()
{
    int a,b=10,c=2;
#pragma omp parallel for default(none) private(a,ricardo_milos) shared(b,c) 
for (int i=0; i<100;i++)
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
