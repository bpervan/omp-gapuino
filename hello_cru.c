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
    int a,b=10,c=2,ricardo_milos = 30;
    int nada = 2000;
#pragma omp parallel for default(none) private(b,ricardo_milos) shared(a,c)
for (int i = 0 ; i < nada; i++  )
{
    a+=b*i;
#pragma omp single
    {   
        
        
        c+=a;





    }
    printf("o valor de a no core %d e: %d\n",a,omp_get_thread_num());
}
function();
    //teste na main
    //outro teste

exit (0);

}

//teste dps da main
