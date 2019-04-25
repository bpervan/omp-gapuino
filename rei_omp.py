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
flagpf = 0
#it = iter(arq1)
library =[]
structures =[]

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
        continue
    elif re.search("pragma",linha) and re.search("omp",linha) and re.search("parallel",linha) and re.search("for",linha):       
        if not re.search("default",linha):
                print(linha)
                print("use default(none) directive to parallel for")
                break;
        else:
                new_linha = re.findall(r'private\((.*?)\)',linha)
                print(new_linha)
                prov_var = new_linha[0].split(',')
                print(prov_var)
                prov_struct = []
                texto.append("estrutura"+str(contador)+" L1_vect"+str(contador))
                texto.append("L1_vect = L1_malloc(CORE_NUMBER*sizeof(estrutura"+str(contador)+")")
                var_len = len(prov_var)
                for vari in range(var_len):
                    prov_struct.append("L1_vect."+str(prov_var[vari])+"="+str(prov_var[vari]))
                structures.append(prov_struct)
        re.sub(' +',' ',linha)
        flagpf = 1
        texto.append("\nparallelfor_function"+str(contador)+"(0)\n")
        print("achei parallel for de numero: "+str(contador)+"\n")

        continue
    elif flagomp: #to dentro de um pragma?
        if(re.search("{",linha)and flagchave == 0):
            flagchave = 1
        elif not flagchave:#a zona paralela é só a próxima linha
            flagomp = 0
            contador = contador +1
            func.append("\n"+linha)
            functions.append(func)
            func = []

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
    elif flagpf:
        if flagpf==1:
                            flagpf=0
        if(re.search("{",linha)and flagchave == 0):
            print("entramos na flagchave\n")
            flagchave = 1
            func.append("new_n = estrutura.n/CORE_NUMBER\n")
        
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
    if re.search("parallel_function",linha):
        arq2.write("CLUSTER_Start(0, CORE_NUMBER);\n")
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *)"+str(contador- cont_paral)+", 0);\n")
        cont_paral = cont_paral - 1
       # arq2.write("printf(\"Waiting..."+"\\"+"n\");\n")
        arq2.write("CLUSTER_Wait(0);\n")
        arq2.write("CLUSTER_Stop(0);\n")
    elif re.search("parallelfor_function",linha):
        arq2.write("CLUSTER_Start(0, CORE_NUMBER);\n")
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *)"+str(contador- cont_paral)+", 0);\n")
        cont_paral = cont_paral - 1
       # arq2.write("printf(\"Waiting..."+"\\"+"n\");\n")
        arq2.write("CLUSTER_Wait(0);\n")
        arq2.write("CLUSTER_Stop(0);\n")

    else:
         arq2.write(linha+"\n")# o fim do arquivo chegou
##for linha_tex in texto:
##    print(linha_tex)
##for lista in functions:
##    for linha_tex in lista:
##        print(linha_tex)
arq1.close()
arq2.close()

