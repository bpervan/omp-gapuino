#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#o script a seguir deve ler e traduzir um codigo em openmp para mbedos
#include "gap_cluster.h"
import sys
import re
title=sys.argv[1]


arq1=open(str(title),'r')

arq2=open("output/"+str(title)+"2.c",'w')


func = []
texto = []
contador = 0;
it = iter(arq1);
for linha in arq1:
    linha=linha.rstrip()
    it = iter(arq1);
    if(re.search("#pragma omp parallel",linha)):
            if re.search("{",) == False:
                func.append(linha);
            else:
                while(re.search
                break;
            else:
                while re.search("}",l1)==False:
                    print("lululululul\n")
    else:
        texto.append(linha);
                

#print(texto)
print("\n")
print(func)
print(contador)
arq2.writelines(texto)
arq1.close()
arq2.close()

