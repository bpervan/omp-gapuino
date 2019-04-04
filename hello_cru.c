#include <stdio.h>
#include <omp.h>
#include "omp_gap8.h"

int main()
{
#pragma omp parallel
printf("Hello fom core %d",omp_get_thread_num());

return 0;
}
