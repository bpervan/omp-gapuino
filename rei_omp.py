#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#o script a seguir deve ler e traduzir um codigo em openmp para mbedos
#include "gap_cluster.h"
import sys
import re
title=sys.argv[1]


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
    if re.search("omp.h", linha):
        continue
    elif re.search("include",linha) or re.search("define",linha):
        library.append(linha)
        continue
    if re.search("pragma omp parallel",linha): #é regiao paralela?
        flagomp = 1
#        print("o que que ta acontecendo aqui?\n")
    elif flagomp: #to dentro de um pragma?
        if (re.search("{",linha)):
                flagchave=1
        if flagchave: #tem chaves na regiao?
                if (re.search("{", linha)): #tem chaves internas?
                    flagchave2=1
                    func.append(linha)
                elif (flagchave2 and re.search("}", linha)): #a chave interna fechou?
                        func.append(linha)
                        flagchave2 = 0
                elif flagchave2:#ainda estou na chave interna
                        func.append(linha)
                elif re.search("}",linha):#a regiao paralela fechou?
                    func.append(linha)
                    flagomp = 0
                    contador = contador + 1
                    functions.append(func)
                    func = []
        else:#so a prox linha e paralela
                func.append("   "+linha)
                flagomp = 0
                functions.append(func)
                func =[]
                contador = contador +1
    else:#nao e regiao paralela
         texto.append(linha)
#lets define the generic functions to be called


for linha in library:
    arq2.write(linha+"\n")
for cont2 in range (contador):
    arq2.write("void generic_function"+str(cont2)+"(void* gen_var"+str(cont2)+"){\n")
    arq2.writelines(functions[cont2])
    arq2.write("\n}\n")
    print(functions[cont2])
    print("\n sou uma piada pra você?\n")
arq2.write("void caller(void* arg){\n")
arq2.write("int x = (int)arg;\n")
for cont2 in range (contador):
        arq2.write("if(x =="+str(cont2)+")return generic_function"+str(cont2)+"(0);\n")
arq2.write("}\n")
arq2.write("\n\n")
arq2.write("void Master_Entry(void *arg) {\n")
arq2.write("    CLUSTER_CoresFork(caller, arg);\n")
arq2.write("}\n")



flag_main=0
flagchave=0
flagchave2=0
for linha in texto:
    linha = linha.rstrip()
    if re.search("main",linha):
        flag_main = 1
    elif flag_main ==1 and linha == "{":
        flag_main = 2
    elif flag_main == 1:
        arq2.write("CLUSTER_Start(0, CORE_NUMBER);\n")
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *) NULL, 0);\n")
        arq2.write("CLUSTER_Wait(0);\n")
        if (re.search("{",linha)):
                flagchave=1
        if flagchave: #tem chaves na regiao?
                if (re.search("{", linha)): #tem chaves internas?
                    flagchave2=1
                    func.append(linha)
                elif (flagchave2 and re.search("}", linha)): #a chave interna fechou?
                        func.append(linha)
                        flagchave2 = 0
                elif flagchave2:#ainda estou na chave interna
                        func.append(linha)
                elif re.search("}",linha):#a regiao paralela fechou?
                    arq2.write("CLUSTER_Stop(0);\n")
                    arq2.write("exit(0);\n")
                    flag_main=0
    elif flag_main ==2:
        if re.search("return",linha):
            arq2.write("exit(0)\n}\n")
        arq2.write("CLUSTER_Start(0, CORE_NUMBER);\n")
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *) NULL, 0);\n")
        arq2.write("CLUSTER_Wait(0);\n")
        if (re.search("{",linha)):
                flagchave=1
        if flagchave: #tem chaves na regiao?
                if (re.search("{", linha)): #tem chaves internas?
                    flagchave2=1
                    func.append(linha)
                elif (flagchave2 and re.search("}", linha)): #a chave interna fechou?
                        func.append(linha)
                        flagchave2 = 0
                elif flagchave2:#ainda estou na chave interna
                        func.append(linha)
                elif re.search("}",linha):#a regiao paralela fechou?
                    arq2.write("CLUSTER_Stop(0);\n")
                    arq2.write("exit(0);\n")
                    
                    flag_main = 0
    arq2.write(linha+"\n")
#arq2.write(
print(texto)
#print("\n")
#print(func)
print(contador)
#print("\n")
print(functions)
#arq2.writelines(texto)
print(library)
#print(arq2)
arq1.close()
arq2.close()

