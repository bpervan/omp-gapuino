#include <stdio.h>
#include "omp_gap8.h"

int main()
{
    int soma=0,a=10,w=5,b=10,c=2,r = 30;
    int nada = 20;

    for (int i = 0 ; i < nada; i++  )
    {
        a+=(b+i);
        printf("%d\n",a);
        c+=a;
        printf("o valor de a no core %d e: %d\n",omp_get_thread_num(),a);
        soma +=b+c;

        printf("soma = %d no core: %d\n", soma, omp_get_thread_num());
    }
    printf("o resultado da soma depois do parallel for1 e: %d\n",soma);

    exit (0);

}
