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
count_parallelfor=0
it_arq1 = iter(arq1)
lista_var_pf=[]
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
                new_linha = re.findall(r'shared\((.*?)\)',linha)
                lista_var_pf.append(new_linha[0].split(','))
                prov_struct = []
                prov_var=[]
                prov_var = re.findall(r'shared\((.*?)\)',linha)[0].split(',')+re.findall(r'private\((.*?)\)',linha)[0].split(',')
                new_linha = re.findall(r'private\((.*?)\)',linha)
                #prov_var = new_linha[0].split(',')
                texto.append("L1_structure"+str(count_parallelfor)+" L1_vect"+str(count_parallelfor)+"\n")
                texto.append("L1_vect = L1_malloc(CORE_NUMBER*sizeof(L1_structure"+str(count_parallelfor)+")\n")
                var_len = len(prov_var) 
                print(prov_var)
                for vari in range(var_len):
                    prov_struct.append("int "+str(prov_var[vari])+"\n")
                texto.append("L1_vect."+str(prov_var[vari])+"="+str(prov_var[vari])+"\n")
                structures.append(prov_struct)
                
        flagpf = 1
        texto.append("\nparallelfor_function"+str(count_parallelfor)+"(0)\n")
        print("achei parallel for de numero: "+str(count_parallelfor)+"\n")
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
    elif flagpf==1:



        #lets seek for iterator var and limmit of iteration
        for_iter = re.findall("(\(.*?\;)",linha)[0]
        print(for_iter)
        for_stop = re.findall("\;.*?\;",linha)[0]
        print(for_stop)
        for_modifier = re.findall("(\;[^\;)]*\))",linha)[0]
        print(for_modifier)
        if re.search(">=",for_stop):
            n = for_stop.split(">=")[1]
            i = for_stop.split(">=")[0]
            operator = ">="
        elif re.search("<=",for_stop):
            n = for_stop.split("<=")[1]
            i = for_stop.split("<=")[0]
            operator = "<="
        elif re.search("!=",for_stop):
            n = for_stop.split("!=")[1]
            i = for_stop.split("!=")[0]
            operator = "!="
        elif re.search("<",for_stop):
            n = for_stop.split("<")[1]
            i = for_stop.split("<")[0]
            operator = "<"
        elif re.search(">",for_stop):
            n = for_stop.split(">")[1]
            i = for_stop.split(">")[0]
            operator = ">"
        n = n.split(";")[0].strip()
        if n.isdigit():
            texto.append("new_n = "+n+"\n")

        print(n)
        i = i.split(";")[1].strip()
        print (i)
        print(operator)
        modifier = for_modifier.split(";")[1].split(")")[0].strip()
        print(modifier)
        starter = for_iter.split("=")[1].split(";")[0].strip()
        print(starter)
        func.append("L1_structure"+str(count_parallelfor)+" L1_structure = (L1_structure"+str(count_parallelfor)+") gen_var"+str(contador)+"\n")
        func.append("int new_n = (L1_structure"+str(count_parallelfor)+"."+str(n)+"/CORE_NUMBER)*(omp_get_thread_num()+1)\n")
        func.append("for(L1_structure."+i+"= ("+str(n)+"/CORE_NUMBER)*omp_get_thread_num(); "+"L1_structure."+i+operator+"new_n;L1_structure."+modifier+")\n{\n")
        flagpf=2
    if flagpf==2:
 


        if(re.search("{",linha)and flagchave == 0):
            flagchave = 1
        elif not flagchave:#a zona paralela é só a próxima linha
            flagpf = 0
            contador = contador +1
            func.append("\n"+linha)
            functions.append(func)
            func = []

        if flagchave:#estamos dentro de uma zona paralela
                func.append(linha+"\n")
                if re.search("{",linha):#tem chaves internas
                        flagchave2=flagchave2+linha.count("{")-linha.count("}")
                        print("o numero de chaves relativo : "+str(flagchave2)+"\n")
                elif re.search("}",linha):
                        flagchave2=flagchave2-linha.count("}")
                        print("o numero de chaves relativo e: "+str(flagchave2)+"\n")
                if(flagchave2==0 and re.search("}",linha)):
                        print("eu sou uma piada para você?\n")
                        flagchave=0
                        flagpf = 0
                        print(linha)
                        contador = contador +1
                        functions.append(func)
                        print(func)
                        func = []
                        print("sai da zona paralela com chaves")
                        count_parallelfor = count_parallelfor+1
    else:#nao e regiao paralela
         texto.append(linha)
#lets define the generic functions to be called


for linha in library:
    arq2.write(linha+"\n")
len_structures = len(structures)
for cont2 in range(len_structures):
    arq2.write("typedef struct L1_structure"+str(cont2)+"{\n")
    arq2.writelines(structures[cont2])
    arq2.write("}L1_structure"+str(cont2)+"\n")
    

for cont2 in range (contador):#escreve as funcoes das zonas paralelas
    arq2.write("void generic_function"+str(cont2)+"(void* gen_var"+str(cont2)+"){\n")
   # if(functions[cont2][0]=="{"):
    #    arq2.write("{\n")
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

