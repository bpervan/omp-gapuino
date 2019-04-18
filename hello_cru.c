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
#pragma omp parallel
printf("Hello fom core %d\n",omp_get_thread_num());
#pragma omp parallel
{
    printf("esse teste veio do core ");
    printf("%d\n",omp_get_thread_num());
}
function();
    //teste na main
    //outro teste

exit (0);

}

//teste dps da main
