#include <stdio.h>
#include <omp.h>
#include "omp_gap8.h"

int main()
{
#pragma omp parallel
printf("Hello fom core %d\n",omp_get_thread_num());
/*teste
 * teste
 * teste
 * teste*/
return 0;
}

//teste dps da main
