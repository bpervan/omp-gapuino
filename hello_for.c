#include <stdio.h>
#include <omp.h>
#include "omp_gap8.h"

int main()
{
    int soma=0,a=10,w=5,b=10,c=2,r = 30;
    int N = 20;

#pragma omp parallel for private(b,r,soma) shared(a,c) reduction(+:soma)
    for (int i = 0 ; i < N; i++  )
    {
#pragma omp critical
        {
            a+=b+i;
            c+=a;
            soma+=b+c;
        }
        printf("o valor de i no core %d e: %d\n",omp_get_thread_num(),i);
        printf("soma = %d no core: %d\n", soma, omp_get_thread_num());
        printf("o resultado da soma depois do parallel for1 e: %d\n",soma);
    }
    exit (0);
}
