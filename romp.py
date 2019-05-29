#!/usr/bin/env python2
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
arq2.write("#include <stdlib.h>\n")
arq2.write("#define CORE_NUMBER   (8)\n")

def hasncb(listx,cont):
    if cont == 0:
        return 0
    elif re.search("{",listx):
        cont=cont+listx.count("{")-listx.count("}")
        return 1
    elif re.search("}",listx):
         cont=cont-listx.count("}")
         return 1




flagchave2 = 0
flagchave = 0
flagomp = 0
func = []
functions=[]
texto = []
contador = 0
flagpf = 0
#it = iter(arq1)
library =[]
structures =[]
it_arq1 = iter(arq1)
lista_var_pf=[]
schedule = 1
prov_vars_private = ""
prov_vars_shared = ""
prov_vars_shared2 = []
list_var=[]
red_oper=""
red_var=""
flag_red=0
flagchave3=0
flagchave4=0
flagvars=0
flagcrit=0
cores=[]
flagcrit2=0
##############################################################################
#               _       __              _ _ _                    _           #
# ___  ___  ___| | __  / _| ___  _ __  | (_) |__  _ __ __ _ _ __(_) ___  ___ #
#/ __|/ _ \/ _ \ |/ / | |_ / _ \| '__| | | | '_ \| '__/ _` | '__| |/ _ \/ __|#
#\__ \  __/  __/   <  |  _| (_) | |    | | | |_) | | | (_| | |  | |  __/\__ \#
#|___/\___|\___|_|\_\ |_|  \___/|_|    |_|_|_.__/|_|  \__,_|_|  |_|\___||___/#
#                                                                            #
##############################################################################
for linha in arq1:
    linha=linha.rstrip()
    if linha.rstrip()=="" or linha.rstrip()=="\n":
            continue
    if re.search("<stdio>", linha):
        continue
    elif re.search("omp.h", linha):
        continue
    elif re.search("include",linha) or re.search("define",linha):
        library.append(linha)
        continue

 ##########################
#seek for pragma critical#
##########################   



    if re.search("pragma",linha)and re.search("omp",linha)and re.search("critical",linha):
        
            flagcrit=1
            func.append("\nEU_MutexLock(0);\n")
            continue
    elif flagcrit==1:
        
        if linha==r"\s*":
            func.append(linha)
            continue
        elif not re.search("{",linha):
            func.append(linha)
            func.append("\nEU_MutexUnlock(0);\n")
            flagcrit=0

            continue
        else:
            print("pq entrou aqui\n")
            func.append(linha)
            flagcrit=2
            flagcrit2=flagcrit2+linha.count("{")-linha.count("}")
            continue
            
    elif flagcrit==2:
        func.append("\n")
        if(flagcrit2==1 and re.search("}",linha)):
                func.append("\nEU_MutexUnlock(0);\n")
                flagcrit=0
                flagcrit2=0
        elif re.search("{",linha):#tem chaves internas
                flagcrit2=flagcrit2+linha.count("{")-linha.count("}")
        elif re.search("}",linha):
                flagcrit2=flagcrit2-linha.count("}")
        

        func.append(linha)



#######################################################################
#                           _       __                                # 
#             ___  ___  ___| | __  / _| ___  _ __                     #
#            / __|/ _ \/ _ \ |/ / | |_ / _ \| '__|                    #
#            \__ \  __/  __/   <  |  _| (_) | |                       #
#            |___/\___|\___|_|\_\ |_|  \___/|_|                       #
#                                                                     #
#                                                                     #
#                                                                     #
#                                                                     #
#                             _ _      _                              #
#       _ __   __ _ _ __ __ _| | | ___| |  _______  _ __   ___  ___   #
#      | '_ \ / _` | '__/ _` | | |/ _ \ | |_  / _ \| '_ \ / _ \/ __|  #
#      | |_) | (_| | | | (_| | | |  __/ |  / / (_) | | | |  __/\__ \  #
#      | .__/ \__,_|_|  \__,_|_|_|\___|_| /___\___/|_| |_|\___||___/  #
#      |_|                                                            #
#                                                                     #
#                                                                     #
#                                                                     #
#                                                                     #
#######################################################################

    #elif re.search("pragma",linha) and re.search("omp",linha)and re.search("parallel",linha) and (not re.search("for",linha)): #é regiao paralela?
    elif re.search(r"pragma\s+omp\s+parallel\s*",linha)and not re.search("for",linha):    
        contador = contador+1
        if re.search("num_threads",linha):
            cores.append(re.findall(r'num_threads\((.*?)\)',linha)[0])
            print(re.findall(r'num_threads\((.*?)\)',linha)[0])
        else:
            cores.append("CORE_NUMBER")
        if re.search(r"private|shared",linha):
                prov_vars_private = re.findall(r'private\((.*?)\)',linha)[0].split(',')
                prov_vars_shared = re.findall(r'shared\((.*?)\)',linha)[0].split(',')

                prov_vars = prov_vars_shared+prov_vars_private
                var_len = len(prov_vars_shared)+ len(prov_vars_private) 
                prov_struct = []
                for vari in range(var_len):
                    prov_struct.append("float "+str(prov_vars[vari])+";\n")
                    lista_var_pf.append(vari)
                    texto.append("estrutura"+str(contador-1)+"."+str(prov_vars[vari])+"="+str(prov_vars[vari])+";\n")
                list_var.append(["nada"])


                structures.append(prov_struct)
                flagvars=1
        else:
                structures.append(["int ignore;\n"])
                structures.append(["int ignores;\n"])
                prov_vars_shared = ["ignore"]
                prov_vars_private = ["ignores"]


        flagomp = 1
        texto.append("parallel_function"+str(contador-1)+"(0)\n")
        
        continue




    #elif re.search("pragma",linha) and re.search("omp",linha) and re.search("parallel",linha) and re.search("for",linha):       
    elif re.search(r"pragma\s+omp\s+parallel\s+for",linha):    
        contador = contador+1
        if re.search("num_threads",linha):
            cores.append(re.findall(r'num_threads\((.*?)\)',linha)[0])
            print(re.findall(r'num_threads\((.*?)\)',linha)[0])
        else:
            cores.append("CORE_NUMBER")
        print("oloco2")
        if not re.search("default",linha):
                print(linha)
                print("use default(none) specifying public and shared variables directive to parallel for")
                break;
        else:
                prov_struct = []

                
                #texto.append("estrutura"+str(contador-1)+"=malloc(CORE_NUMBER*sizeof(L1_structure"+str(contador-1)+"));\n")

               ##############################################################
        #######verivy if have a reduction clause and identify the variable #########
               #############################################################
                if re.search("reduction",linha) or re.search("reduction\(",linha):
                    reduct = re.findall(r'reduction\((.+)\)',linha)[0].split(":")
                    red_oper = reduct[0]
                    red_var = reduct[1]
                    flag_red = 1
                prov_vars_private = re.findall(r'private\((.*?)\)',linha)[0].split(',')
                prov_vars_shared = re.findall(r'shared\((.*?)\)',linha)[0].split(',')



              #  for i in prov_vars_shared:
              #      prov_vars_shared2.append(i+"\s*=\s*"   )
              #      prov_vars_shared2.append(i+"\s*\+=\s*" )
              #      prov_vars_shared2.append(i+"\s*-=\s*"  )
              #      prov_vars_shared2.append(i+"\s*\*=\s*" )
              #      prov_vars_shared2.append(i+"\s*=\s*"   )
              #      prov_vars_shared2.append(i+"\s*\+\+\s*")
              #      prov_vars_shared2.append(i+"\s*--\s*"  )
              #  print(prov_vars_shared2)
                prov_vars = prov_vars_shared+prov_vars_private
                var_len = len(prov_vars_shared)+ len(prov_vars_private) 
                for vari in range(var_len):
                    prov_struct.append("float "+str(prov_vars[vari])+";\n")
                    lista_var_pf.append(vari)
                    texto.append("estrutura"+str(contador-1)+"."+str(prov_vars[vari])+"="+str(prov_vars[vari])+";\n")

                list_var.append(prov_vars_shared)
               # print(prov_struct)
                structures.append(prov_struct)
                flagpf=1
                continue

#############################################################
#                                               _ _      _  #
#  ___  _ __ ___  _ __    _ __   __ _ _ __ __ _| | | ___| | #
# / _ \| '_ ` _ \| '_ \  | '_ \ / _` | '__/ _` | | |/ _ \ | #
#| (_) | | | | | | |_) | | |_) | (_| | | | (_| | | |  __/ | #
# \___/|_| |_| |_| .__/  | .__/ \__,_|_|  \__,_|_|_|\___|_| #
#                |_|     |_|                                #
#############################################################


    elif flagomp==1 and not flagcrit: #to dentro de um pragma?
        

        
        print(flagchave)

        if linha==r"\s*":
            func.append(linha)
            continue
        if re.search("pragma",linha) and re.search("omp",linha) and re.search("single",linha):
            func.append("EU_MutexLock(0);\n")
            func.append("if(++x_flagsingle_x==1)\n")
            func.append("EU_MutexUnlock(0);\n")
            continue

        elif not re.search("parallel",linha) and re.search("pragma",linha) and re.search("omp",linha) and re.search("for",linha):
            flagomp=2
            continue
        elif(re.search("{",linha)and flagchave == 0):
            flagchave = 1
            continue
        elif not flagchave:#a zona paralela é só a próxima linha
            flagomp = 0
            
            func.append("\n"+linha)
            func.append("\n}")
            functions.append(func)
            func = []
        elif flagchave:#estamos dentro de uma zona paralela
            func.append(linha+"\n")
            print("valor de flagchave2:\n")
            print(flagchave2)
            if(flagchave2==0 and re.search("}",linha)):
                flagchave=0
                flagomp = 0
                if flagvars:
                    rp = re.compile(r'\b({})\b'.format('|'.join(prov_vars_private)))
                    rs = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared)))
                

                    func2=[]
                    for prov_line in func:
                        if re.search("\"",prov_line):
                            prov2_line = prov_line.split("\"")
                            prov3_line = ''.join(rp.sub(r"L1_structure.\1",prov_line)).split("\"")
                            func2.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                            continue
                        func2.append(''.join(rp.sub(r"L1_structure.\1",prov_line)))
                    func3=[]
                    
                    
                    
                    
                    for prov_line in func2:
                        structu="estrutura"+str(contador-1)+"."
                        if re.search("\"",prov_line):
                            prov2_line = prov_line.split("\"")

                            prov3_line = ''.join(rs.sub("estrutura"+str(contador-1)+'.'+r'\1',prov_line)).split("\"")
                            func3.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                            continue
                        func3.append(''.join(rs.sub("estrutura"+str(contador-1)+'.'+r'\1',prov_line)))
                    
                    for it in prov_vars_shared:
                        texto.append(it+"=estrutura"+str(contador-1)+"."+it+";\n")
                    
                    
                    
                    
                    
                    
                    if flag_red:
                        func3.append("CLUSTER_SynchBarrier();\n")
                        func3.append("EU_MutexLock(0);\n")
                        func3.append("\nestrutura"+str(contador-1)+"."+red_var+"=estrutura"+str(contador-1)+"."+red_var+red_oper+"L1_structure."+red_var+";\n")
                        func3.append("EU_MutexUnlock(0);\n")
                        texto.append(red_var+"="+red_var+red_oper+"estrutura"+str(contador-1)+"."+red_var+";\n")
                        functions.append(func3)
                        func2 = []
                        prov_vars_shared = []
                        prov_vars_private = []
                        prov_vars = []

                    functions.append(func3)
                    func2 = []
                    prov_vars_shared = []
                    prov_vars_private = []
                    prov_vars = []


            elif re.search("{",linha):#tem chaves internas
                    flagchave2=flagchave2+linha.count("{")-linha.count("}")
            elif re.search("}",linha):
                    flagchave2=flagchave2-linha.count("}")
    elif flagomp==2 and not flagcrit:
   
            
            #lets seek for iterator var and limmit of iteration
            for_iter = re.findall("(\(.*\;)",linha)[0]
            for_stop = re.findall("\;.*\;",linha)[0]
            for_modifier = re.findall("(\;[^\;)]*\))",linha)[0]
    
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
    
            i = i.split(";")[1].strip()
            modifier = for_modifier.split(";")[1].split(")")[0].strip()
            starter = for_iter.split("=")[1].split(";")[0].strip()

                #########################################
           ######appending the new for function parallel#########
                #########################################

            func.append("L1_structure"+str(contador-1)+" L1_structure;\n")
            func.append("L1_structure = estrutura"+str(contador-1)+";\n")
            func.append("int new_n = (L1_structure."+str(n)+"/CORE_NUMBER)*(omp_get_thread_num()+1);\n")
            func.append("if (omp_get_thread_num()==CORE_NUMBER-1)new_n = new_n+ L1_structure."+str(n)+"%CORE_NUMBER;\n")
            #if re.search("int",for_iter):
                #texto.append("int "+i+";\n" )
           #     func.append("for(int "+i+"= "+str(starter)+"+(L1_structure."+str(n)+"/CORE_NUMBER)*omp_get_thread_num();\n")
            #    func.append("for("+i+"; "+i+operator+"new_n;"+modifier+")\n{\n")
            #else:

            func.append("int "+i+"= "+str(starter)+"+(L1_structure."+str(n)+"/CORE_NUMBER)*omp_get_thread_num();\n")
            func.append("for("+i+";"+i+operator+"new_n;"+modifier+")\n\n")
            ##texto.append("estrutura"+str(contador-1)+"."+i+"= "+i+";\n")
            texto.append("estrutura"+str(contador-1)+"."+str(n)+" = "+str(n)+";\n")
    #need no more append the for limmits
            structures[contador-1].append("int "+str(n)+";\n")
            flagomp=1
    
            continue
    
    
##############################################################################
#                                               _ _      _    __             #
#  ___  _ __ ___  _ __    _ __   __ _ _ __ __ _| | | ___| |  / _| ___  _ __  #
# / _ \| '_ ` _ \| '_ \  | '_ \ / _` | '__/ _` | | |/ _ \ | | |_ / _ \| '__| #
#| (_) | | | | | | |_) | | |_) | (_| | | | (_| | | |  __/ | |  _| (_) | |    #
# \___/|_| |_| |_| .__/  | .__/ \__,_|_|  \__,_|_|_|\___|_| |_|  \___/|_|    #
#                |_|     |_|                                                 #
#                                                                            # 
##############################################################################

    elif flagpf==1 and not flagcrit:



        #lets seek for iterator var and limmit of iteration
        for_iter = re.findall("(\(.*\;)",linha)[0]
        for_stop = re.findall("\;.*\;",linha)[0]
        for_modifier = re.findall("(\;[^\;)]*\))",linha)[0]

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

        i = i.split(";")[1].strip()
        modifier = for_modifier.split(";")[1].split(")")[0].strip()
        starter = for_iter.split("=")[1].split(";")[0].strip()
            #########################################
       ######appending the new for function parallel#########
            #########################################
        func.append("L1_structure"+str(contador-1)+" L1_structure;\n")
        func.append("L1_structure = estrutura"+str(contador-1)+";\n")
        func.append("int new_n = (L1_structure."+str(n)+"/CORE_NUMBER)*(omp_get_thread_num()+1);\n")
        func.append("if (omp_get_thread_num()==CORE_NUMBER-1)new_n = new_n+ L1_structure."+str(n)+"%CORE_NUMBER;\n")
#        if re.search("int",for_iter):
 #           #texto.append("int "+i+";\n" )
 #j           func.append("for(int "+i+"= "+str(starter)+"+(L1_structure."+str(n)+"/CORE_NUMBER)*omp_get_thread_num(); "+i+operator+"new_n;"+modifier+")\n{\n")
  #      else:
        #func.append("int "+i+"=L1_structure"+str(contador-1)+"."+i+"="+str(starter)+"+ (L1_structure."+str(n)+"/CORE_NUMBER)*omp_get_thread_num();\n")

        func.append("int "+i+"= "+str(starter)+"+(L1_structure."+str(n)+"/CORE_NUMBER)*omp_get_thread_num();\n")
        func.append("for("+i+";"+i+operator+"new_n; i"+modifier.split(i)[1]+")\n\n")
        texto.append("estrutura"+str(contador-1)+"."+str(n)+" = "+str(n)+";\n")
        texto.append("\nparallelfor_function"+str(contador-1)+"(0)\n")
        structures[contador-1].append("int "+str(n)+";\n")
        if re.search(r"\)\s*{",linha):
            flagchave3=1
        flagpf=2
        continue




    elif flagpf==2 and not flagcrit:

        if re.search("pragma",linha)and re.search("omp",linha) and re.search("single",linha):
            func.append("EU_MutexLock(0);\n")
            func.append("if(++x_flagsingle_x==1)\n")
            func.append("EU_MutexUnlock(0);\n")
            continue
        if linha=="\s*":
            func.append(linha)
            continue

        elif(re.search("{",linha)and flagchave3 == 0):
            func.append(linha)
            flagchave3 = 1
            continue
        elif not flagchave3:#o for é só a próxima linha
            #replacing shared variables with actual structure
            flagpf = 0
            func.append("\n"+linha+"\n")
            func.append("\n}\n")
            functions.append(func)
            func = []




        elif flagchave3:#estamos dentro de um for paralelo
                rp = re.compile(r'\b({})\b'.format('|'.join(prov_vars_private)))
                rs = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared)))
 #               rs2 = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared2)))
               # print(rs.pattern)
 #               print(rs2.pattern)
##                if rs2.findall(linha) !=[]:
#                    func.append("EU_MutexLock(0);\n")
#                    func.append("\n"+linha+"\n")
#                    func.append("EU_MutexUnlock(0);\n")
#                else:
                func.append("\n"+linha+"\n")
                
                
                if(flagchave4==0 and re.search("}",linha)):

                        rs = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared)))
                        flagchave3=0
                        flagpf = 0
                        #print(prov_vars_shared)
                        func2=[]
                        
                        
                        
                        for prov_line in func:
                            if re.search("\"",prov_line):
                                prov2_line = prov_line.split("\"")
                                prov3_line = ''.join(rp.sub(r"L1_structure.\1",prov_line)).split("\"")
                                func2.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                continue
                            func2.append(''.join(rp.sub(r"L1_structure.\1",prov_line)))
                        func3=[]
                        
                        
                        
                        
                        for prov_line in func2:
                            structu="estrutura"+str(contador-1)+"."
                            if re.search("\"",prov_line):
                                prov2_line = prov_line.split("\"")

                                prov3_line = ''.join(rs.sub("estrutura"+str(contador-1)+'.'+r'\1',prov_line)).split("\"")
                                func3.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                continue
                            func3.append(''.join(rs.sub("estrutura"+str(contador-1)+'.'+r'\1',prov_line)))
                        
                        
                        
                        
                        for it in prov_vars_shared:
                            texto.append(it+"=estrutura"+str(contador-1)+"."+it+";\n")
                    

                        
                        
                        
                        if flag_red:
                            func3.append("CLUSTER_SynchBarrier();\n")
                            func3.append("EU_MutexLock(0);\n")
                            
                            func3.append("\nestrutura"+str(contador-1)+"."+red_var+"=estrutura"+str(contador-1)+"."+red_var+red_oper+"L1_structure."+red_var+";\n")
                            func3.append("EU_MutexUnlock(0);\n")
                            texto.append(red_var+"="+red_var+red_oper+"estrutura"+str(contador-1)+"."+red_var+";\n")
                        func3.append("\n}\n")
                        functions.append(func3)
                        func = []
                        func2 = []
                        flagchave3=0
                        prov_vars_shared = []
                        prov_vars_private = []
                        prov_vars = []
                elif re.search("{",linha):#tem chaves internas
                        flagchave4=flagchave4+linha.count("{")-linha.count("}")
                elif re.search("}",linha):
                        flagchave4=flagchave4-linha.count("}")






    else:#nao e regiao paralela
         texto.append(linha)
#lets define the generic functions to be called
print("contador eh: \n")
print(contador)
#####################################
#               _ _   _             #  
#__      ___ __(_) |_(_)_ __   __ _ # 
#\ \ /\ / / '__| | __| | '_ \ / _` |# 
# \ V  V /| |  | | |_| | | | | (_| |# 
#  \_/\_/ |_|  |_|\__|_|_| |_|\__, |#  
#                             |___/ #  
#                                   #  
# _ __   _____      __              #    
#| '_ \ / _ \ \ /\ / /              #
#| | | |  __/\ V  V /               #  
#|_| |_|\___| \_/\_/                #    
#                                   #   
# _____ _ _                         #
#|  ___(_) | ___                    # 
#| |_  | | |/ _ \                   #
#|  _| | | |  __/                   #
#|_|   |_|_|\___|                   #
#                                   #
#####################################

print("a quantidade de funcoes e: "+str(len(functions)) )

for linha in library:
    arq2.write(linha+"\n")
len_structures = len(structures)


for cont2 in range(len_structures):
    arq2.write("typedef struct L1_structure"+str(cont2)+"{\n")
    #structures[cont2].append("int IDstructure;\n")
    arq2.writelines(structures[cont2])
    arq2.write("}L1_structure"+str(cont2)+";\n")
    arq2.write("L1_structure"+str(cont2)+" estrutura"+str(cont2)+";\n")
arq2.write("int x_flagsingle_x=0;\n")


for cont2 in range (contador):#escreve as funcoes das zonas paralelas
    arq2.write("void generic_function"+str(cont2)+"(void* gen_var"+str(cont2)+");\n")

arq2.write("void caller(void* arg){\n")
arq2.write("int x = (int)arg;\n")
for cont2 in range (contador):
    arq2.write("if(x =="+str(cont2)+")return generic_function"+str(cont2)+"((void*)x);\n")
arq2.write("}\n")
arq2.write("\n\n")
arq2.write("void Master_Entry(void *arg) {\n")
arq2.write("    CLUSTER_CoresFork(caller, arg);\n")
arq2.write("}\n")
contshare = len(list_var)
contshare2= contshare
count2pf = contador-1
cont_paral = contador-1
for linha in texto:
    #ligando e desligando o cluster
    if re.search("parallel_function",linha):
        arq2.write("CLUSTER_Start(0,"+cores[contador-1- cont_paral] +");\n")
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *)"+str(contador-1- cont_paral)+", 0);\n")
        cont_paral = cont_paral - 1
        arq2.write("CLUSTER_Wait(0);\n")
        arq2.write("CLUSTER_Stop(0);\n")
        arq2.write("int x_flagsingle_x=0;\n")

    elif re.search("parallelfor_function",linha):
        arq2.write("CLUSTER_Start(0,"+cores[contador-1- cont_paral] +");\n")
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *)"+str(contador-1- cont_paral)+", 0);\n")
        arq2.write("CLUSTER_Wait(0);\n")
        cont_paral = cont_paral - 1
        count2pf = count2pf-1
        arq2.write("CLUSTER_Stop(0);\n")
        arq2.write("int x_flagsingle_x=0;\n")

    else:
         arq2.write(linha+"\n")# o fim do arquivo chegou
for cont2 in range (contador):#escreve as funcoes das zonas paralelas
    arq2.write("void generic_function"+str(cont2)+"(void* gen_var"+str(cont2)+"){\n")
    print("buga em: "+str(cont2)+"\n")
    arq2.writelines(functions[cont2])
    arq2.write("\n")

        
arq1.close()
arq2.close()
