EQUENCES
test = open (r"/Users/lasyamarla/SIB_BLAST_sequence.ssp")
sequenceslist=[]
sequences = []

for line in test:
	i = 0
	while line[i] == ' ':
		i+=1 
	if line[i] == 'S' and line[i+1] == 'E':
		wordset = line.split()
		sequenceslist.append(wordset[1]) 

sequences = ''.join(sequenceslist)

k=0
if sequences[k] == '0' or sequences[k] == '1' or sequences[k] == '2' or sequences[k] == '3' or sequences[k] == '4' or sequences[k] == '5' or sequences[k] == '6' or sequences[k] == '7' or sequences[k] == '8' or sequences[k] == '9':  
	sequences.replace(sequences[k],"")
	k+=1

print "SEQ:" + sequences

#NEWRAW
test = open (r"/Users/lasyamarla/SIB_BLAST_sequence.ssp")
newrawlist=[]
newraw = []

for line in test:
	i = 0
	while line[i] == ' ':
		i+=1 
	if line[i] == 'N' and line[i+4] == 'R':
		wordset = line.split()
		newrawlist.append(wordset[1]) 

newraw = ''.join(newrawlist)

k=0
if newraw[k] == '0' or newraw[k] == '1' or newraw[k] == '2' or newraw[k] == '3' or newraw[k] == '4' or newraw[k] == '5' or newraw[k] == '6' or newraw[k] == '7' or newraw[k] == '8' or newraw[k] == '9':  
	newraw.replace(newraw[k],"")


#NEWCAP
test = open (r"/Users/lasyamarla/SIB_BLAST_sequence.ssp")
newcaplist=[]
newcap = []

for line in test:
	i = 0
	while line[i] == ' ':
		i+=1 
	if line[i] == 'N' and line[i+4] == 'C':
		wordset = line.split()
		newcaplist.append(wordset[1]) 

newcap = ''.join(newcaplist)
k=0
if newcap[k] == '0' or newcap[k] == '1' or newcap[k] == '2' or newcap[k] == '3' or newcap[k] == '4' or newcap[k] == '5' or newcap[k] == '6' or newcap[k] == '7' or newcap[k] == '8' or newcap[k] == '9':  	
	newcap.replace(newcap[k],"")
	k+=1


#PORTER
test = open (r"/Users/lasyamarla/SIB_BLAST_sequence.ssp")
porterlist=[]
porter = []

for line in test:
	i =0
	while line[i] == ' ':
		i+=1 
	if line[i] == 'P' and line[i+1] == 'O':
		wordset = line.split()
		porterlist.append(wordset[1]) 

porter = ''.join(porterlist)

k=0
while (k < len(porter)):
	if porter[k] != 'c' and porter[k] != 'E' and porter[k] != 'H':
		porter = porter.replace(porter[k], "") 
		
	k+=1



test = open (r"/Users/lasyamarla/SIB_BLAST_sequence.ssp")

ssprolist=[]
sspro = []

for line in test:
	i =0
	while line[i] == ' ':
		i+=1 
	if line[i] == 'S' and line[i+1] == 'S':
		wordset = line.split()
		ssprolist.append(wordset[1]) 

sspro = ''.join(ssprolist)

k=0
while (k < len(sspro)):
	if sspro[k] != "c" and sspro[k] != "E" and sspro[k] != "H":
		sspro = sspro.replace(sspro[k], "") 
		
	k+=1



# APSSP2 
test = open (r"/Users/lasyamarla/SIB_BLAST_sequence.ssp")
apssp2list=[]
apssp2 = []


for line in test:
	i =0
	while line[i] == ' ':
		i+=1 
	if line[i] == 'A':
		wordset = line.split()
		apssp2list.append(wordset[1]) 

apssp2 = ''.join(apssp2list)

k=0
while (k < len(apssp2)):
	if apssp2[k] != "c" and apssp2[k] != "E" and apssp2[k] != "H":
		apssp2 = apssp2.replace(apssp2[k], "") 
		
	k+=1





#PSIPRED
test = open (r"/Users/lasyamarla/SIB_BLAST_sequence.ssp")
psipredlist=[]
psipred = []

for line in test:
	i =0
	while line[i] == ' ':
		i+=1 
	if line[i] == 'P' and line[i+1] == 'S':
		wordset = line.split()
		psipredlist.append(wordset[1]) 

psipred = ''.join(psipredlist)	

k=0
while (k < len(psipred)):
	if psipred[k] != 'c' and psipred[k] != 'E' and psipred[k] != 'H':
		psipred = psipred.replace(psipred[k], "") 
		
	k+=1




#JPRED
test = open (r"/Users/lasyamarla/SIB_BLAST_sequence.ssp")

jpredlist=[]
jpred = []

for line in test:
	i =0
	while line[i] == ' ':
		i+=1 
	if line[i] == 'J':
		wordset = line.split()
		jpredlist.append(wordset[1]) 
jpred = ''.join(jpredlist)

k=0
while (k < len(jpred)):
	if jpred[k] != 'c' and jpred[k] != 'E' and jpred[k] != 'H':
		jpred = jpred.replace(jpred[k], "") 
		
	k+=1

 

#OLDRAW
test = open (r"/Users/lasyamarla/SIB_BLAST_sequence.ssp")
oldrawlist=[]
oldraw = []

for line in test:
	i =0
	while line[i] == ' ':
		i+=1 
	if line[i] == 'O' and line[i+4] == 'R':
		wordset = line.split()
		oldrawlist.append(wordset[1]) 

oldraw = ''.join(oldrawlist)

k=0
while (k < len(oldraw)):
	if oldraw[k] != 'c' and oldraw[k] != 'E' and oldraw[k] != 'H' and oldraw[k] != '-':
		oldraw = oldraw.replace(oldraw[k], "") 
		
	k+=1

oldraw = ''.join(oldrawlist)



#OLDCAP
test = open (r"/Users/lasyamarla/SIB_BLAST_sequence.ssp")
oldcaplist=[]
oldcap = []

for line in test:
	i =0
	while line[i] == ' ':
		i+=1 
	if line[i] == 'O' and line[i+4] == 'R':
		wordset = line.split()
		oldcaplist.append(wordset[1]) 

oldcap = ''.join(oldcaplist)
k=0
while (k < len(oldcap)):
	if oldcap[k] != 'c' and oldcap[k] != 'E' and oldcap[k] != 'H' and oldcap != '-':
		oldcap = oldcap.replace(oldcap[k], "") 
		
	k+=1

bigarray = []
k=0

while k<len(newraw):
	if newraw[k] == 'H':
		Harray = []
		while newraw[k] == 'H': 
			Harray.append(k) 
			k+=1
			if newraw[k] != 'H':
				bigarray.append(Harray)
	else: 
		k+=1

#getting array of 6 indexes to check before H's 
indicesarray=[]
k = 0 
while k< len(bigarray):
	m=0
	num1=(bigarray[k])[0]
	while m<6:
		num1=num1-1
		indicesarray.append(num1)
		m+=1
	k+=1

#getting arrays of 6 numbers to check after H's 
k = 0 
while k< len(bigarray):
	m=0
	num1=(bigarray[k])[len(bigarray[k])-1]
	while m<6:
		num1=num1+1
		indicesarray.append(num1)
		m+=1
	k+=1

k=0
while k<len(indicesarray):
	m=indicesarray[k]
	threecheckerarray=[]
	if porter[m]=='H':
		threecheckerarray.append(k)		
	if apssp2[m]=='H':
		threecheckerarray.append(k)
	if sspro[m]=='H':
		threecheckerarray.append(k)	
	if psipred[m]=='H':
		threecheckerarray.append(k)
	if jpred[m]=='H':
		threecheckerarray.append(k)

	if len(threecheckerarray)>=3:
		indicestochange.append(k)
	k+=1

k=0
while (k<len(indicestochange)):
	if newcap[indicestochange[k]] == '-' or newcap[indicestochange[k]] == '?' 
		newcap[indicestochange[k]] == 'H'

print newcap 





