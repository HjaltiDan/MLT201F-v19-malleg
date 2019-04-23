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

##### dir_to_filelist() lýkur #####


def filelist_to_dict(filelist):
	filedict = {}
	for filename in filelist:
		tree = ET.parse(filename)
		root = tree.getroot()
		for entry in root.iter():
		#Hoppum framhjá þessu hrikalega "www.tei-c.org/..../}w" tagi og veljum bara lokastafinn
			if entry.tag.endswith("w"):
				#Fundum orð. Athugum hvort það er til nú þegar		
				potential_lemma = entry.attrib["lemma"]
				#Ef orðið var ekki til, búum til dict færslu fyrir það
				# með orðið sem lykil og mörkun sem gildið		
				if entry.attrib["lemma"] not in filedict:
					filedict[potential_lemma] = entry.attrib["type"]
	return filedict

##### filelist_to_dict() lýkur #####


def file_to_dict(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	filedict = {}

	for entry in root.iter():
	#Hoppum framhjá þessu hrikalega "www.tei-c.org/..../}w" tagi og veljum bara lokastafinn
		if entry.tag.endswith("w"):
			#Fundum nýtt orð. Búum til dict færslu og lykil		
			potential_lemma = entry.attrib["lemma"]		
			if entry.attrib["lemma"] not in filedict:
				filedict[potential_lemma] = entry.attrib["type"]
	return filedict


##### file_to_dict() lýkur #####


def clean_dict(d):
#Hreinsar úr dictionary öll þau gildi sem munu aldrei vera íðorð
#Ath:: Python (sérstaklega 3.6+) er skiljanlega ósátt við að maður
# breyti mutable fyrirbæri sem er *líka* verið að ítra yfir.
# Lausnin gæti valdið einhverjum overhead - sjáum til - 
# en við afritum a.m.k. keys í lista, ítrum yfir *hann* og
# ef eitthvað stak í listanum uppfyllir "ekki í lagi" skilyrðin
# þá notum við .pop(stakið, None) til að henda því úr dictionary
# (Skemmtilega afdráttarlaus lesning á cito.github.io/blog/never-iterate-a-changing-dict
# þar sem hann útskýrir þetta á einfaldan máta og býður upp á
# sömu lausn og, í raun, allir aðrir með sama vandamál.

	#Búum til lista úr keys í viðkomandi dictionary
	keylist = list(d.keys())
	#ATH: Spurning hvort við fáum hraðvirkari kóða ef við erum
	# sniðug með unpacking syntax úr P3.5+ og segjum frekar
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

##### clean_dict() lýkur #####



def filter_dict(returndict, comparedict):
#Ef orð er til í báðum orðabókum hendum við því úr returndict. Skilum henni svo.

#Ath: Í Python 3.5+ gætum við notað nýtt syntax, z = {**x, **y}
#Sleppum því hér til að lenda ekki í einhverju óútskýranlegu veseni

	for i in returndict:	
		if i in comparedict:
			#Notum pop() frekar en del[] því það seinna er ekki atomic
			# (þ.e. gæti keyrt 1+ aðgerð bak við tjöld, ekki bara 1 hreina)
			#Notum svo None í pop() til að Python kasti pottþétt ekki KeyError villu 			
			returndict.pop(i, None)
			break
	return returndict


##### filter_dict() lýkur #####


##### Forritskeyrsla hefst #####

#Búum til lista af öllum XML skrám í 'fotbolti möppunni
fot_list = dir_to_filelist(DIR_FOT)

#Með listanum, búum til dictionary af öllum flettiorðum úr öllum þessum skrám
fotdict = filelist_to_dict(fot_list)

#Gerum það sama fyrir bændablaðið og fyrir alþingisræður
alt_list = dir_to_filelist(DIR_ALT)
altdict = filelist_to_dict(alt_list)
bae_list = dir_to_filelist(DIR_BAE)
baedict = filelist_to_dict(bae_list)

#Hreinsum óþarfa drasl úr öllum orðabókum, enda engin þörf á að láta lokaútkomuna
# innihalda hrat sem er ekki mögulega íðorð
#(ATH: Tékkum hér hvort við lendum nokkuð í veseni með ítrun á mutable object)
fotdict2 = clean_dict(fotdict)
altdict2 = clean_dict(altdict)
baedict2 = clean_dict(baedict)

#Hendum öllum orðum úr fótboltaorðabók sem komu fyrir á Alþingi
#Hendum svo öllu úr fótboltaorðabók sem kom fyrir í Bændablaðinu
fotdict = filter_dict(fotdict, altdict)
fotdict = filter_dict(fotdict, baedict)

#Tímabundinn Python3 kóði sem prentar út lykla og gildi í dict
#for k, v in fotdict.items():
#	print(k, v)

##### Forritskeyrslu lýkur #####

