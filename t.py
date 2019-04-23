#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os

DIR_FOT = 'fotbolti'
DIR_ALT = 'althingi'
DIR_BAE = 'baendabladid'


def dir_to_filelist(dirname):
	filenamelist = []
	for root, dirs, files in os.walk(dirname):
		#print(root)
		for filename in files:
			fullpath = dirname + "/" + filename
			filenamelist.append(fullpath)
		break
	return filenamelist

##### dir_to_filelist() l�kur #####


def filelist_to_dict(filelist):
	filedict = {}
	for filename in filelist:
		tree = ET.parse(filename)
		root = tree.getroot()
		for entry in root.iter():
		#Hoppum framhj� �essu hrikalega "www.tei-c.org/..../}w" tagi og veljum bara lokastafinn
			if entry.tag.endswith("w"):
				#Fundum or�. Athugum hvort �a� er til n� �egar		
				potential_lemma = entry.attrib["lemma"]
				#Ef or�i� var ekki til, b�um til dict f�rslu fyrir �a�
				# me� or�i� sem lykil og m�rkun sem gildi�		
				if entry.attrib["lemma"] not in filedict:
					filedict[potential_lemma] = entry.attrib["type"]
	return filedict

##### filelist_to_dict() l�kur #####


def file_to_dict(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	filedict = {}

	for entry in root.iter():
	#Hoppum framhj� �essu hrikalega "www.tei-c.org/..../}w" tagi og veljum bara lokastafinn
		if entry.tag.endswith("w"):
			#Fundum n�tt or�. B�um til dict f�rslu og lykil		
			potential_lemma = entry.attrib["lemma"]		
			if entry.attrib["lemma"] not in filedict:
				filedict[potential_lemma] = entry.attrib["type"]
	return filedict


##### file_to_dict() l�kur #####


def clean_dict(d):
#Hreinsar �r dictionary �ll �au gildi sem munu aldrei vera ��or�
#Ath:: Python (s�rstaklega 3.6+) er skiljanlega �s�tt vi� a� ma�ur
# breyti mutable fyrirb�ri sem er *l�ka* veri� a� �tra yfir.
# Lausnin g�ti valdi� einhverjum overhead - sj�um til - 
# en vi� afritum a.m.k. keys � lista, �trum yfir *hann* og
# ef eitthva� stak � listanum uppfyllir "ekki � lagi" skilyr�in
# �� notum vi� .pop(staki�, None) til a� henda �v� �r dictionary
# (Skemmtilega afdr�ttarlaus lesning � cito.github.io/blog/never-iterate-a-changing-dict
# �ar sem hann �tsk�rir �etta � einfaldan m�ta og b��ur upp �
# s�mu lausn og, � raun, allir a�rir me� sama vandam�l.

	#B�um til lista �r keys � vi�komandi dictionary
	keylist = list(d.keys())
	#ATH: Spurning hvort vi� f�um hra�virkari k��a ef vi� erum
	# sni�ug me� unpacking syntax �r P3.5+ og segjum frekar
	# keylist = [*.d.keys()]

	for s in keylist:
		l = len(s)
		i = d[s]
		
		if i[:1] == "f" or \
		i[-2:] == "-s" or \
		i[1:] == 'e' or \
		(i[1:] != "a" and l <= 1) or \
		i[:1] == "t":
			print("Popping the key and item pair:")
			print(s)
			print(i)
			d.pop(s, i)
	return d

##### clean_dict() l�kur #####



def filter_dict(returndict, comparedict):
#Ef or� er til � b��um or�ab�kum hendum vi� �v� �r returndict. Skilum henni svo.

#Ath: � Python 3.5+ g�tum vi� nota� n�tt syntax, z = {**x, **y}
#Sleppum �v� h�r til a� lenda ekki � einhverju ��tsk�ranlegu veseni

	for i in returndict:	
		if i in comparedict:
			#Notum pop() frekar en del[] �v� �a� seinna er ekki atomic
			# (�.e. g�ti keyrt 1+ a�ger� bak vi� tj�ld, ekki bara 1 hreina)
			#Notum svo None � pop() til a� Python kasti pott��tt ekki KeyError villu 			
			returndict.pop(i, None)
			break
	return returndict


##### filter_dict() l�kur #####


##### Forritskeyrsla hefst #####

#B�um til lista af �llum XML skr�m � 'fotbolti m�ppunni
fot_list = dir_to_filelist(DIR_FOT)

#Me� listanum, b�um til dictionary af �llum flettior�um �r �llum �essum skr�m
fotdict = filelist_to_dict(fot_list)

#Gerum �a� sama fyrir b�ndabla�i� og fyrir al�ingisr��ur
alt_list = dir_to_filelist(DIR_ALT)
altdict = filelist_to_dict(alt_list)
bae_list = dir_to_filelist(DIR_BAE)
baedict = filelist_to_dict(bae_list)

#Hreinsum ��arfa drasl �r �llum or�ab�kum, enda engin ��rf � a� l�ta loka�tkomuna
# innihalda hrat sem er ekki m�gulega ��or�
#(ATH: T�kkum h�r hvort vi� lendum nokku� � veseni me� �trun � mutable object)
fotdict2 = clean_dict(fotdict)
altdict2 = clean_dict(altdict)
baedict2 = clean_dict(baedict)

#Hendum �llum or�um �r f�tboltaor�ab�k sem komu fyrir � Al�ingi
#Hendum svo �llu �r f�tboltaor�ab�k sem kom fyrir � B�ndabla�inu
fotdict = filter_dict(fotdict, altdict)
fotdict = filter_dict(fotdict, baedict)

#T�mabundinn Python3 k��i sem prentar �t lykla og gildi � dict
#for k, v in fotdict.items():
#	print(k, v)

##### Forritskeyrslu l�kur #####

