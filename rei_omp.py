#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#The follow script is a parser to read OpenMP in GAP8
#include "gap_cluster.h"
import sys
import re
title=sys.argv[1]
#teste

arq1=open(str(title),'r')

title2 = title.split(".c")[0]
arq2=open("output/"+str(title2)+"_gap.c",'w')

arq2.write("#include "+ "\"gap_common.h\"\n")
arq2.write("#include "+"\"gap_cluster.h\"\n")
arq2.write("#define CORE_NUMBER   (8)\n")



flag_hasSh=0
flag_hasPr=0
flagchave2 = 0
flagchave = 0
flagomp = 0
func = []
functions=[]
new_file = []
contador = 0
flagpf = 0
library =[]
structures =[]
it_arq1 = iter(arq1)
lista_var_pf=[]
schedule = 1
prov_vars_private = []
prov_vars_shared = []
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
flagsingle=0
flagsingle2=0


##############################################################################
#               _       __              _ _ _                    _           #
# ___  ___  ___| | __  / _| ___  _ __  | (_) |__  _ __ __ _ _ __(_) ___  ___ #
#/ __|/ _ \/ _ \ |/ / | |_ / _ \| '__| | | | '_ \| '__/ _` | '__| |/ _ \/ __|#
#\__ \  __/  __/   <  |  _| (_) | |    | | | |_) | | | (_| | |  | |  __/\__ \#
#|___/\___|\___|_|\_\ |_|  \___/|_|    |_|_|_.__/|_|  \__,_|_|  |_|\___||___/#
#                                                                            #
##############################################################################
print("always remember to declare all private and shared vars\n")
for r_line in arq1:
#    r_line=r_line.rstrip()
#    if r_line.rstrip()=="" or r_line.rstrip()=="\n":
#            continue
    if re.search("<stdio>", r_line):
        continue
    elif re.search("omp.h", r_line):
        continue
    elif re.search("include",r_line) or re.search("define",r_line):
        library.append(r_line)
        continue

##########################
#seek for pragma critical#
##########################   

    if re.search("#\s*pragma\s+omp\s+critical",r_line):


            flagcrit=1
            func.append("\nEU_MutexLock(0);\n")
            continue
    elif flagcrit==1:
        if r_line==r"\s*":
            func.append(r_line)
            continue
        elif not re.search("{",r_line):
            func.append(r_line)
            func.append("\nEU_MutexUnlock(0);\n")
            flagcrit=0

            continue
        else:
            func.append(r_line)
            flagcrit=2
            flagcrit2=flagcrit2+r_line.count("{")-r_line.count("}")
            continue
            
    if flagcrit==2:
        
        func.append("\n"+r_line+"\n")

        if(flagcrit2+r_line.count("{")==r_line.count("}")):
                func.append("\nEU_MutexUnlock(0);\n")
                flagcrit=0
                flagcrit2=0
                continue
        else: 
                flagcrit2=flagcrit2+r_line.count("{")-r_line.count("}")
                continue


########################
#seek for pragma single#
########################   



    if re.search("#\s*pragma\s+omp\s+single",r_line):


            func.append("EU_MutexLock(0);\n")
            func.append("if(++x_flagsingle_x==1)\n")
            flagsingle=1
            continue
    elif flagsingle==1:
        if r_line==r"\s*":
            func.append(r_line)
            continue
        elif not re.search("{",r_line):
            func.append(r_line)
            func.append("\nEU_MutexUnlock(0);\n")
            flagsingle=0

            continue
        else:
            func.append(r_line)
            flagsingle=2
            flagsingle2=flagsingle2+r_line.count("{")-r_line.count("}")
            continue
            
    elif flagsingle==2:

        func.append("\n"+r_line+"\n")
        if(flagsingle2+r_line.count("{") == r_line.count("}")):
            func.append("\nEU_MutexUnlock(0);\n")
            func.append("CLUSTER_SynchBarrier();\n");
            func.append("x_flagsingle_x=0;\n")
            flagsingle2=0
            flagsingle=0
        else:
            flagsingle2=flagsingle2+r_line.count("{")-r_line.count("}")

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

    

    elif re.search(r"pragma\s+omp\s+parallel\s*",r_line)and not re.search("for",r_line):    
        contador = contador+1
        if re.search("num_threads",r_line):
            cores.append(re.findall(r'num_threads\((.*?)\)',r_line)[0])
            new_file.append("cores_num["+str(contador-1)+"]="+re.findall(r'num_threads\((.*?)\)',r_line)[0]+";\n")
            new_file.append("romp_cores="+cores[contador-1]+";\n")

        else:
            cores.append("CORE_NUMBER")
            new_file.append("cores_num["+str(contador-1)+"]=CORE_NUMBER;\n")
            new_file.append("romp_cores="+cores[contador-1]+";\n")
        if re.search(r"private",r_line):
                prov_vars_private =prov_vars_private + re.findall(r'private\((.*?)\)',r_line)[0].split(',')
                flag_hasPr=1

        if re.search(r"shared",r_line):
                prov_vars_shared = prov_vars_shared + re.findall(r'shared\((.*?)\)',r_line)[0].split(',')
                flag_hasSh=1
        prov_vars = prov_vars_shared+prov_vars_private
        var_len = len(prov_vars_shared)+ len(prov_vars_private) 
        prov_struct = []
        for vari in range(var_len):
            prov_struct.append("float "+str(prov_vars[vari])+";\n")
            lista_var_pf.append(vari)
            new_file.append("romp_global_structure"+str(contador-1)+"."+str(prov_vars[vari])+"="+str(prov_vars[vari])+";\n")

        structures.append(prov_struct)
        if re.search("reduction",r_line) or re.search("reduction\(",r_line):
            reduct = re.findall(r'reduction\((.+)\)',r_line)[0].split(":")
            red_oper = reduct[0]
            red_var = reduct[1]
            flag_red = 1
            new_file.append("romp_global_structure"+str(contador-1)+"."+red_var+"="+red_var+";\n")
        prov_struct = []
        prov_vars = prov_vars_shared+prov_vars_private
        var_len = len(prov_vars_shared)+ len(prov_vars_private) 
        for vari in range(var_len):
            prov_struct.append("float "+str(prov_vars[vari])+";\n")
            lista_var_pf.append(vari)
            new_file.append("romp_global_structure"+str(contador-1)+"."+str(prov_vars[vari])+"="+str(prov_vars[vari])+";\n")

        structures.append(prov_struct)
        flagomp = 1
        new_file.append("parallel_function"+str(contador-1)+"(0)\n")
        continue






###########################
#  seek for parallel for  #
###########################




    elif re.search(r"pragma\s+omp\s+parallel\s+for",r_line):    
        contador = contador+1
        if re.search("num_threads",r_line):
            cores.append(re.findall(r'num_threads\((.*?)\)',r_line)[0])
            print(re.findall(r'num_threads\((.*?)\)',r_line)[0])
            new_file.append("romp_cores="+cores[contador-1]+";\n")
            
        else:
            cores.append("CORE_NUMBER")
            new_file.append("cores_num["+str(contador-1)+"]=CORE_NUMBER;\n")
            new_file.append("romp_cores="+cores[contador-1]+";\n")

        if(re.search(r"private\s*\(.+\)",r_line)):

            prov_vars_private = prov_vars_private + re.findall(r'private\((.*?)\)',r_line)[0].split(',')
            print(prov_vars_private)
            flag_hasPr=1

        if(re.search(r"shared\s*\(.+\)",r_line)):

            prov_vars_shared = prov_vars_shared + re.findall(r'shared\((.*?)\)',r_line)[0].split(',')
            print(prov_vars_shared)

            flag_hasSh=1


            ################################################################## 
        #######verivy if have a reduction clause and identify the variable #########
               #############################################################


        if re.search("reduction",r_line) or re.search("reduction\(",r_line):
            reduct = re.findall(r'reduction\((.+)\)',r_line)[0].split(":")
            red_oper = reduct[0]
            red_var = reduct[1]
            flag_red = 1
            new_file.append("romp_global_structure"+str(contador-1)+"."+red_var+"="+red_var+";\n")
        prov_struct = []
        prov_vars = prov_vars_shared+prov_vars_private
        var_len = len(prov_vars_shared)+ len(prov_vars_private) 
        for vari in range(var_len):
            prov_struct.append("float "+str(prov_vars[vari])+";\n")
            lista_var_pf.append(vari)
            new_file.append("romp_global_structure"+str(contador-1)+"."+str(prov_vars[vari])+"="+str(prov_vars[vari])+";\n")

        list_var.append(prov_vars_shared)
        structures.append(prov_struct)
        flagpf=1
        continue




      #  for i in prov_vars_shared:
      #      prov_vars_shared2.append(i+"\s*=\s*"   )
      #      prov_vars_shared2.append(i+"\s*\+=\s*" )
      #      prov_vars_shared2.append(i+"\s*-=\s*"  )
      #      prov_vars_shared2.append(i+"\s*\*=\s*" )
      #      prov_vars_shared2.append(i+"\s*=\s*"   )
      #      prov_vars_shared2.append(i+"\s*\+\+\s*")
      #      prov_vars_shared2.append(i+"\s*--\s*"  )
      #  print(prov_vars_shared2)


        

#############################################################
#                                               _ _      _  #
#  ___  _ __ ___  _ __    _ __   __ _ _ __ __ _| | | ___| | #
# / _ \| '_ ` _ \| '_ \  | '_ \ / _` | '__/ _` | | |/ _ \ | #
#| (_) | | | | | | |_) | | |_) | (_| | | | (_| | | |  __/ | #
# \___/|_| |_| |_| .__/  | .__/ \__,_|_|  \__,_|_|_|\___|_| #
#                |_|     |_|                                #
#############################################################


    elif flagomp==1 and not flagcrit: #to dentro de um pragma?
        #r_line = re.sub("omp_get_num_threads()","cores_num["+str(contador-1)+"]",r_line)
        if r_line==r"\s*":
            func.append(r_line)
            continue

        elif(re.search("{",r_line)and flagchave == 0):
            func.append(r_line)
            flagchave = 1
            continue
        elif not flagchave:#o for é só a próxima r_line
            ##################################################
   ##########replacing shared variables with actual structure###########
            ##################################################
                        
                        flagomp = 0
                        func.append("\n"+r_line+"\n")
                        func.append("\n}\n")
                        functions.append(func)
                        func = []

        elif flagchave:#estamos dentro de um for paralelo
 #               rs2 = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared2)))
               # print(rs.pattern)
 #               print(rs2.pattern)
##                if rs2.findall(r_line) !=[]:
#                    func.append("EU_MutexLock(0);\n")
#                    func.append("\n"+r_line+"\n")
#                    func.append("EU_MutexUnlock(0);\n")
#                else:
                func.append("\n"+r_line+"\n")
                
                
                if(flagchave2==0 and re.search("}",r_line)):
                        func3=[]
                        if(flag_hasSh and not flag_hasPr):
                            rs = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared)))
                            for prov_line in func:
                                structu="romp_global_structure"+str(contador-1)+"."
                                if re.search("\"",prov_line):
                                    prov2_line = prov_line.split("\"")
                                    prov3_line = ''.join(rs.sub("romp_global_structure"+str(contador-1)+'.'+r'\1',prov_line)).split("\"")
                                    func3.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                    continue
                                func3.append(''.join(rs.sub("romp_global_structure"+str(contador-1)+'.'+r'\1',prov_line)))
                            for it in prov_vars_shared:
                                new_file.append(it+"=romp_global_structure"+str(contador-1)+"."+it+";\n")



                        #print(prov_vars_shared)
#                        func4=[]
#                        for provline in func:
#                            func4.append(re.sub(r"omp_get_num_threads()","romp_global_structure"+str(contador-1)+".num_cores",provline))
                        if(not flag_hasSh and flag_hasPr):
                        
                            rp = re.compile(r'\b({})\b'.format('|'.join(prov_vars_private)))
                            for prov_line in func:
                                if re.search("\"",prov_line):
                                    prov2_line = prov_line.split("\"")
                                    prov3_line = ''.join(rp.sub(r"L1_structure.\1",prov_line)).split("\"")
                                    func3.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                    continue
                                func3.append(''.join(rp.sub(r"L1_structure.\1",prov_line)))
                        
                        
                        if(flag_hasSh and flag_hasPr):
                            func2 = []
                            rp = re.compile(r'\b({})\b'.format('|'.join(prov_vars_private)))
                            for prov_line in func:
                                if re.search("\"",prov_line):
                                    prov2_line = prov_line.split("\"")
                                    prov3_line = ''.join(rp.sub(r"L1_structure.\1",prov_line)).split("\"")
                                    func2.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                    continue
                                func2.append(''.join(rp.sub(r"L1_structure.\1",prov_line)))
                        
                            rs = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared)))

                            for prov_line in func2:
                                structu="romp_global_structure"+str(contador-1)+"."
                                if re.search("\"",prov_line):
                                    prov2_line = prov_line.split("\"")
                                    prov3_line = ''.join(rs.sub("romp_global_structure"+str(contador-1)+'.'+r'\1',prov_line)).split("\"")
                                    func3.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                    continue
                                func3.append(''.join(rs.sub("romp_global_structure"+str(contador-1)+'.'+r'\1',prov_line)))
                            for it in prov_vars_shared:
                                new_file.append(it+"=romp_global_structure"+str(contador-1)+"."+it+";\n")


                        
                        
                    

                        
                        
                        
                        if flag_red:
                            func3.append("EU_MutexLock(0);\n")
                           # structures[contador-1].append("float "+red_var+";\n")
                            func3.append("\nromp_global_structure"+str(contador-1)+"."+red_var+"=romp_global_structure"+str(contador-1)+"."+red_var+red_oper+"L1_structure."+red_var+";\n")
                            func3.append("EU_MutexUnlock(0);\n")
                            new_file.append(red_var+"="+red_var+red_oper+"romp_global_structure"+str(contador-1)+"."+red_var+";\n")
                            flag_red=0
                        flag_hasSh=0
                        flag_hasPr=0
                        func3.append("\n}\n")
                        functions.append(func3)
                        func = []
                        func4=[]
                        func2 = []
                        flagchave=0
                        prov_vars_shared = []
                        prov_vars_private = []
                        prov_vars = []
                elif re.search("{",r_line):#tem chaves internas
                        flagchave2=flagchave2+r_line.count("{")-r_line.count("}")
                elif re.search("}",r_line):
                        flagchave2=flagchave2-r_line.count("}")
    elif flagomp==2 and not flagcrit:
            if r_line==r"\s*":
                func.append(r_line)
                continue

  
            #r_line = re.sub("omp_get_num_threads()","cores_num["+str(contador-1)+"]",r_line)
            
            #lets seek for iterator var and limmit of iteration
            for_iter = re.findall("(\(.*\;)",r_line)[0]
            for_stop = re.findall("\;.*\;",r_line)[0]
            for_modifier = re.findall("(\;[^\;)]*\))",r_line)[0]
    
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
                new_file.append("new_n = "+n+"\n")
    
            i = i.split(";")[1].strip()
            modifier = for_modifier.split(";")[1].split(")")[0].strip()
            starter = for_iter.split("=")[1].split(";")[0].strip()

                #########################################
           ######appending the new for function parallel#########
                #########################################

            func.append("L1_structure"+str(contador-1)+" L1_structure;\n")
            func.append("L1_structure = romp_global_structure"+str(contador-1)+";\n")
            func.append("int new_n = (L1_structure."+str(n)+"/CORE_NUMBER)*(omp_get_thread_num()+1);\n")
            func.append("if (omp_get_thread_num()<L1_structure."+str(n)+"%cores_num["+str(contador-1)+"])new_n++;\n")

            func.append("int "+i+"= "+str(starter)+"+(L1_structure."+str(n)+"/CORE_NUMBER)*omp_get_thread_num();\n")
            func.append("for("+i+";"+i+operator+"new_n;"+modifier+")\n\n")
            new_file.append("romp_global_structure"+str(contador-1)+"."+str(n)+" = "+str(n)+";\n")
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

        #r_line = re.sub("omp_get_num_threads()","cores_num["+str(contador-1)+"]",r_line)

        if r_line==r"\s*":
                func.append(r_line)
                continue

        #lets seek for iterator var and limmit of iteration
        for_iter = re.findall("(\(.*\;)",r_line)[0]
        for_stop = re.findall("\;.*\;",r_line)[0]
        for_modifier = re.findall("(\;[^\;)]*\))",r_line)[0]

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
            new_file.append("new_n = "+n+"\n")

        i = i.split(";")[1].strip()
        modifier = for_modifier.split(";")[1].split(")")[0].strip()
        starter = for_iter.split("=")[1].split(";")[0].strip()
            #########################################
       ######appending the new for function parallel#########
            #########################################
        func.append("L1_structure"+str(contador-1)+" L1_structure;\n")
        func.append("L1_structure = romp_global_structure"+str(contador-1)+";\n")
        func.append("int new_n = (L1_structure."+str(n)+"/CORE_NUMBER)*(omp_get_thread_num()+1);\n")
        func.append("if (omp_get_thread_num()<L1_structure."+str(n)+"%cores_num["+str(contador-1)+"])new_n++;\n")


#        if re.search("int",for_iter):
 #           #new_file.append("int "+i+";\n" )
 #j           func.append("for(int "+i+"= "+str(starter)+"+(L1_structure."+str(n)+"/CORE_NUMBER)*omp_get_thread_num(); "+i+operator+"new_n;"+modifier+")\n{\n")
  #      else:
        #func.append("int "+i+"=L1_structure"+str(contador-1)+"."+i+"="+str(starter)+"+ (L1_structure."+str(n)+"/CORE_NUMBER)*omp_get_thread_num();\n")

        func.append("int "+i+"= "+str(starter)+"+(L1_structure."+str(n)+"/CORE_NUMBER)*omp_get_thread_num();\n")
        func.append("for("+i+";"+i+operator+"new_n; i"+modifier.split(i)[1]+")\n\n")
        new_file.append("romp_global_structure"+str(contador-1)+"."+str(n)+" = "+str(n)+";\n")
        new_file.append("\nparallelfor_function"+str(contador-1)+"(0)\n")
        structures[contador-1].append("int "+str(n)+";\n")
        if re.search(r"\)\s*{",r_line):
            flagchave3=1
        flagpf=2
        continue




    elif flagpf==2 and not flagcrit:

        #r_line = re.sub("omp_get_num_threads()","cores_num["+str(contador-1)+"]",r_line)
        if r_line==r"\s*":
            func.append(r_line)
            continue

        elif(re.search("{",r_line)and flagchave3 == 0):
            func.append(r_line)
            flagchave3 = 1
            continue
        elif not flagchave3:#o for é só a próxima r_line
            ##################################################
   ##########replacing shared variables with actual structure###########
            ##################################################
                        
                        flagpf = 0
                        func.append("\n"+r_line+"\n")
                        func.append("\n}\n")
                        functions.append(func)
                        func = []




        elif flagchave3:#estamos dentro de um for paralelo
 #               rs2 = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared2)))
               # print(rs.pattern)
 #               print(rs2.pattern)
##                if rs2.findall(r_line) !=[]:
#                    func.append("EU_MutexLock(0);\n")
#                    func.append("\n"+r_line+"\n")
#                    func.append("EU_MutexUnlock(0);\n")
#                else:
                func.append("\n"+r_line+"\n")
                
                
                if(flagchave4==0 and re.search("}",r_line)):
                        func3=[]
                        if(flag_hasSh and not flag_hasPr):
                            rs = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared)))
                            for prov_line in func:
                                structu="romp_global_structure"+str(contador-1)+"."
                                if re.search("\"",prov_line):
                                    prov2_line = prov_line.split("\"")
                                    prov3_line = ''.join(rs.sub("romp_global_structure"+str(contador-1)+'.'+r'\1',prov_line)).split("\"")
                                    func3.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                    continue
                                func3.append(''.join(rs.sub("romp_global_structure"+str(contador-1)+'.'+r'\1',prov_line)))
                            for it in prov_vars_shared:
                                new_file.append(it+"=romp_global_structure"+str(contador-1)+"."+it+";\n")

                        #print(prov_vars_shared)
#                        func4=[]
#                        for provline in func:
#                            func4.append(re.sub(r"omp_get_num_threads()","romp_global_structure"+str(contador-1)+".num_cores",provline))
                        if(not flag_hasSh and flag_hasPr):
                        
                            rp = re.compile(r'\b({})\b'.format('|'.join(prov_vars_private)))
                            for prov_line in func:
                                if re.search("\"",prov_line):
                                    prov2_line = prov_line.split("\"")
                                    prov3_line = ''.join(rp.sub(r"L1_structure.\1",prov_line)).split("\"")
                                    func3.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                    continue
                                func3.append(''.join(rp.sub(r"L1_structure.\1",prov_line)))
                        
                        if(flag_hasSh and flag_hasPr):
                            func2 = []
                            rp = re.compile(r'\b({})\b'.format('|'.join(prov_vars_private)))
                            for prov_line in func:
                                if re.search("\"",prov_line):
                                    prov2_line = prov_line.split("\"")
                                    prov3_line = ''.join(rp.sub(r"L1_structure.\1",prov_line)).split("\"")
                                    func2.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                    continue
                                func2.append(''.join(rp.sub(r"L1_structure.\1",prov_line)))
                        
                            rs = re.compile(r'\b({})\b'.format('|'.join(prov_vars_shared)))

                            for prov_line in func2:
                                structu="romp_global_structure"+str(contador-1)+"."
                                if re.search("\"",prov_line):
                                    prov2_line = prov_line.split("\"")
                                    prov3_line = ''.join(rs.sub("romp_global_structure"+str(contador-1)+'.'+r'\1',prov_line)).split("\"")
                                    func3.append(prov3_line[0]+"\""+prov2_line[1]+"\""+prov3_line[2])
                                    continue
                                func3.append(''.join(rs.sub("romp_global_structure"+str(contador-1)+'.'+r'\1',prov_line)))
                            for it in prov_vars_shared:
                                new_file.append(it+"=romp_global_structure"+str(contador-1)+"."+it+";\n")
                        
                        if flag_red:
                            func3.append("EU_MutexLock(0);\n")
                            
                           # structures[contador-1].append("float "+red_var+";\n")
                            func3.append("\nromp_global_structure"+str(contador-1)+"."+red_var+"=romp_global_structure"+str(contador-1)+"."+red_var+red_oper+"L1_structure."+red_var+";\n")
                            func3.append("EU_MutexUnlock(0);\n")
                            new_file.append(red_var+"="+red_var+red_oper+"romp_global_structure"+str(contador-1)+"."+red_var+";\n")
                            flag_red=0
                        flag_hasSh=0
                        flag_hasPr=0
                        func3.append("\n}\n")
                        functions.append(func3)
                        func = []
                        func4=[]
                        func2 = []
                        flagpf=0
                        flagchave3=0
                        prov_vars_shared = []
                        prov_vars_private = []
                        prov_vars = []
                elif re.search("{",r_line): # there are internal brackets
                        flagchave4=flagchave4+r_line.count("{")-r_line.count("}")
                elif re.search("}",r_line):
                        flagchave4=flagchave4-r_line.count("}")

    else: # not a parallel region
         new_file.append(r_line)
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

for r_line in library:
    arq2.write(r_line+"\n")

len_structures = len(structures)

for cont2 in range(len_structures):
    arq2.write("typedef struct L1_structure"+str(cont2)+"{\n")
    #structures[cont2].append("int IDstructure;\n")
    arq2.writelines(structures[cont2])
    arq2.write("int num_cores;\n")
    arq2.write("}L1_structure"+str(cont2)+";\n")
    arq2.write("L1_structure"+str(cont2)+" romp_global_structure"+str(cont2)+";\n")

arq2.write("int x_flagsingle_x=0;\n")
arq2.write("int romp_cores=CORE_NUMBER;\n")
arq2.write("int cores_num["+str(contador)+"];\n")

for cont2 in range (contador): # writes the parallel zones functions
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

for r_line in new_file:
    # turning the cluster on and off
    if re.search("parallel_function",r_line):
        arq2.write("CLUSTER_Start(0,"+cores[contador-1- cont_paral] +");\n")
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *)"+str(contador-1- cont_paral)+", 0);\n")
        cont_paral = cont_paral - 1
        arq2.write("CLUSTER_Wait(0);\n")
        arq2.write("CLUSTER_Stop(0);\n")
        arq2.write("x_flagsingle_x=0;\n")
        arq2.write("romp_cores=CORE_NUMBER;\n")

    elif re.search("parallelfor_function",r_line):
        arq2.write("CLUSTER_Start(0,"+cores[contador-1- cont_paral] +");\n")
        arq2.write("CLUSTER_SendTask(0, Master_Entry, (void *)"+str(contador-1- cont_paral)+", 0);\n")
        arq2.write("CLUSTER_Wait(0);\n")
        cont_paral = cont_paral - 1
        count2pf = count2pf-1
        arq2.write("CLUSTER_Stop(0);\n")
        arq2.write("x_flagsingle_x=0;\n")
        arq2.write("romp_cores=CORE_NUMBER;\n")

    else:
         arq2.write(r_line+"\n") 

for cont2 in range (contador): # writes parallel zones functions
    arq2.write("void generic_function"+str(cont2)+"(void* gen_var"+str(cont2)+"){\n")
    arq2.writelines(functions[cont2])
    arq2.write("\n")

        
arq1.close()
arq2.close()
