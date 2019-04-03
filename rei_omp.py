#!/usr/bin/env python2
# -*- coding: utf-8 -*-
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
    if "#pragma omp parallel" in linha:
        arq2.write("CLUSTER_Start(0, CORE_NUMBER)\n");
        arq2.write("");
        contador = contador+1
        #continue
    else:
        arq2.write(linha+'\n')
print(texto)
print(contador)
arq2.writelines(texto)
arq1.close()
arq2.close()

