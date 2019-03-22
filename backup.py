#o script a seguir deve ler e traduzir um codigo em openmp para mbedos

import sys
import re
title=sys.argv[1]


arq1=open(str(title),'r')

arq2=(str(title)+"2.c",'w')

texto = []
linha = []

linha.append(arq1.readline())

for line in arq1:
	if re.search("#pragma",str(linha)) and re.search("omp",str(linha)):
		if re.search("parallel",str(linha)):
			texto.append("Thread thread"+str(line))
#		print("colera do dragao")
	else:
		texto.append(linha)
		texto.append("\n")
	texto.append("\n")
	linha=[]
	linha.append(arq1.readline())
arq2.writelines(texto)

