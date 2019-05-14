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
    int soma=0,a,b=10,c=2,r = 30;
    int nada = 2000;
#pragma omp parallel for default(none) private(b,r,soma) shared(a,c) reduction(+:soma)
for (int i = 0 ; i < nada; i++  )
{
    a+=b+i;
#pragma omp single
    {   
        c+=a;
    }
    printf("o valor de a no core %d e: %d\n",omp_get_thread_num(),a);
    soma+=b+c;
}
#pragma omp parallel for default(none) private(b,r,soma) shared(a,c) reduction(*:soma)
for (int j = 0 ; i < nada; i++  )
{
    a+=1;
    soma*=2;
}
function();
    //teste na main
    //outro teste
printf("o resultado da soma e %d\n",soma);
exit (0);

}

//teste dps da main
