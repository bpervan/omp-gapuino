#o script a seguir deve ler e traduzir um codigo em openmp para mbedos
#include "gap_cluster.h"
import sys
import re
title=sys.argv[1]


arq1=open(str(title),'r')

arq2=open("output/"+str(title)+"2.c",'w')

texto = []
contador = 0;
for linha in arq1:
    linha=linha.rstrip()
    linha.sub("omp_get_thread_num()","CORE_NUMBER")
    if "parallel" in linha:
        arq2.write("Thread thread\n ")
        contador = contador+1
        #continue
    else:
        arq2.write(linha+'\n')
print(texto)
print(contador)
arq2.writelines(texto)
arq1.close()
arq2.close()

