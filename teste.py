#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import regex as re
texto=[]
texto.append("int a,b,c;\n")
texto.append("{\n")
texto.append("\ta=b+c;\n")
var=[]
var.append("a")
var.append("b")
var.append("c")

texto.append("}\n")
for line in texto:
  for vari in var:
      line = re.sub(vari+"=","L1_structure."+vari+"=",line.rstrip())
      line = re.sub(vari+">","L1_structure."+vari+">",line.rstrip())
      line = re.sub(vari+"<","L1_structure."+vari+"<",line.rstrip())
      line = re.sub(vari+"\+","L1_structure."+vari+"+",line.rstrip())
      line = re.sub(vari+"\-","L1_structure."+vari+"-",line.rstrip())
      line = re.sub(vari+"\*","L1_structure."+vari+"*",line.rstrip())
      line = re.sub(vari+"\/","L1_structure."+vari+"/",line.rstrip())
      line = re.sub("="+vari,"L1_structure."+vari,line.rstrip())
      line = re.sub(">"+vari,"L1_structure."+vari,line.rstrip())
      line = re.sub("<"+vari,"L1_structure."+vari,line.rstrip())
      line = re.sub("\+"+vari,"L1_structure."+vari,line.rstrip())
      line = re.sub("\-"+vari,"L1_structure."+vari,line.rstrip())
      line = re.sub("\*"+vari,"L1_structure."+vari,line.rstrip())
      line = re.sub("\/"+vari,"L1_structure."+vari,line.rstrip())
      teste.append(line)
for line in teste:
      print(line)
