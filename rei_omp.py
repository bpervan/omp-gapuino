#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#o script a seguir deve ler e traduzir um codigo em openmp para mbedos
#include "gap_cluster.h"
import sys
import re
title=sys.argv[1]
#teste

arq1=open(str(title),'r')

title2 = title.split(".c")[0]
arq2=open("output/"+str(title2)+"_gap.c",'w')

arq2.write("#include "+"\"cmsis.h\"\n")
arq2.write("#include "+ "\"gap_common.h\"\n")
arq2.write("#include "+"\"mbed_wait_api.h\"\n")

arq2.write("// FEATURE_CLUSTER\n")
arq2.write("#include "+"\"gap_cluster.h\"\n")
arq2.write("#include "+"\"gap_dmamchan.h\"\n")
arq2.write("#include "+"<time.h>\n")

arq2.write("#define CORE_NUMBER   (8)\n")



flagchave = 0
flagchave2 = 0
flagomp = 0
func = []
functions=[]
texto = []
contador = 0

it = iter(arq1)
library =[]
for linha in arq1:
    linha=linha.rstrip()
    if "<stdio>" in linha:
        continue
    elif re.search("omp.h", linha):
        continue
    elif re.search("include",linha) or re.search("define",linha):
        library.append(linha)
        continue
    if re.search("pragma",linha) and re.search("omp",linha)and re.search("parallel",linha) and (not re.search("for",linha)): #é regiao paralela?
        flagomp = 1
        texto.append("\nparallel_function"+str(contador)+"(0)\n")
        print("entrei na zona paralela")
        continue
    elif flagomp: #to dentro de um pragma?
        if(re.search("{",linha)and flagchave == 0):
            print("entramos na flagchave\n")
            flagchave = 1
        elif not flagchave:#a zona paralela é só a próxima linha
            flagomp = 0
            print(linha)
            contador = contador +1
            func.append("\n"+linha)
            functions.append(func)
            func = []
            print("sai da zona paralela")

        if flagchave:#estamos dentro de uma zona paralela
                func.append(linha+"\n")
                print(linha+"\n")
                if re.search("{",linha):#tem chaves internas
                        flagchave2=flagchave2+linha.count("{")-linha.count("}")
                        print("o numero de chaves relativo : "+str(flagchave2)+"\n")
                elif re.search("}",linha):
                        flagchave2=flagchave2-linha.count("}")
                        print("o numero de chaves relativo e: "+str(flagchave2)+"\n")
                if(flagchave2==0 and re.search("}",linha)):
                        print("eu sou uma piada para você?\n")
                        flagchave=0
                        flagomp = 0
                        print(linha)
                        contador = contador +1
                        functions.append(func)
                        print(func)
                        func = []
                        print("sai da zona paralela com chaves")
    else:#nao e regiao paralela
         texto.append(linha)
#lets define the generic functions to be called


for linha in library:
    arq2.write(linha+"\n")
for cont2 in range (contador):#escreve as funcoes das zonas paralelas
    arq2.write("void generic_function"+str(cont2)+"(void* gen_var"+str(cont2)+"){\n")
    if(functions[cont2][0]=="{"):
        arq2.write("{\n")
    arq2.writelines(functions[cont2])
    arq2.write("\n}\n")
arq2.write("void caller(void* arg){\n")
arq2.write("int x = (int)arg;\n")
for cont2 in range (contador):
        arq2.write("if(x =="+str(cont2)+")return generic_function"+str(cont2)+"(0);\n")
arq2.write("}\n")
arq2.write("\n\n")
arq2.write("void Master_Entry(void *arg) {\n")
arq2.write("    CLUSTER_CoresFork(caller, arg);\n")
arq2.write("}\n")


cont_paral =contador
flag_main=0
flagchave=0
flagchave2=0
for linha in texto:
    if re.search("parallel",linha):
        arq2.write("CLUSTER_Start(0, CORE_NUMBER);\n")
      #  arq2.write("int *L1_mem = L1_Malloc(8);\n")
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *)"+str(contador- cont_paral)+", 0);\n")
        cont_paral = cont_paral - 1

        arq2.write("printf(\"Waiting..."+"\\"+"n\");\n")
        arq2.write("CLUSTER_Wait(0);\n")
        arq2.write("CLUSTER_Stop(0);\n")
    if re.search("main",linha) and re.search("{",linha):
        flag_main = 1# chave ao lado da main
        arq.write(linha)
        flag_main = 3
        continue
    elif re.search("main",linha):
        flag_main = 2#chave abaixo da main
        arq2.write(linha+"\n")
        continue
    elif flag_main ==2 and re.search("{",linha):
         flag_main = 3
         arq2.write(linha+"\n")
         continue
  #  elif flag_main == 3:
  #       flag_main = 4
  #       continue
    if flag_main == 3:
         #print("sera q ta entrando aqui?")
         if (re.search("{", linha)): #tem chaves internas?
            flagchave2=flagchave2+1
            arq2.write(linha)
         elif (flagchave2 and re.search("}", linha)): #a chave interna fechou?
            arq2.write(linha)
            flagchave2 = flagchave2-1
         elif flagchave2 == 1:#ainda estou na chave interna
            arq2.write(linha)
         elif re.search("}",linha):#fim da main
            print("votz chegou aqui e agora?\n")
            flag_main=0
            arq2.write("exit(0);\n}\n")
            print("exit(0);\n}\n)") 
    else:
         arq2.write(linha)# escreva as demais funções abaixo da main, todas as paralelas estao abaixo
# o fim do arquivo chegou
   #arq2.write(
for linha_tex in texto:
    print(linha_tex)
#print(texto)
#print("\n")
#print(func)
#print(contador)
#print("\n")
#print(functions)
#arq2.writelines(texto)
#print(library)
#print(arq2)
arq1.close()
arq2.close()

