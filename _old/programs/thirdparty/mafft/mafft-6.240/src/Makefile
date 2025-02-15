PREFIX = /project/Biogroup/Software/mafft/lib/mafft
#CC = gcc  -O0  -g -pg 
CC = gcc -O3
#CC = gcc    -mno-cygwin -O3 # for cygwin
#CC = icc -fast              # for icc on Intel
#CC = icc -O3 -ipo -static   # for icc on AMD
#CC = gcc -fast
#CC = gcc  -g -O0 -pg 
LIBS = -lm 

INSTALL = install

PROGS = dvtditr dndfast7 dndblast sextet5 mafft-distance pairalign pairlocalalign \
		pair2hat3s multi2hat3s \
        splittbfast disttbfast tbfast mafft-profile f2cl countlen \
		score getlag dndpre dndpre2 setcore
SCRIPTS = mafft mafft-homologs.rb
OBJCOUNTLEN = mtxutl.o io.o countlen.o defs.o
OBJF2CL = mtxutl.o io.o f2cl.o constants.o defs.o
OBJMULTI2HAT3S = mtxutl.o io.o mltaln9.o tddis.o constants.o \
				 multi2hat3s.o defs.o fft.o fftFunctions.o
OBJPAIR2HAT3S = mtxutl.o io.o mltaln9.o tddis.o constants.o \
				pair2hat3s.o defs.o fft.o fftFunctions.o
OBJPAIRLOCALALIGN = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		            Falign.o MSalignmm.o Galign11.o MSalign11.o suboptalign11.o VAAalign11.o genalign11.o Lalign11.o SAalignmm.o \
					Calignm1.o pairlocalalign.o defs.o fft.o fftFunctions.o
OBJPAIRALIGN = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		            Galign11.o Falign.o Falign_localhom.o Salign11.o SAalignmm.o Calignm1.o \
			        MSalignmm.o pairalign.o defs.o fft.o fftFunctions.o
OBJDUMMY = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		    Falign.o Falign_localhom.o Galign11.o SAalignmm.o Calignm1.o MSalignmm.o \
			disttbfast_dummy.o dummy.o defs.o fft.o fftFunctions.o
OBJSPLITFROMALN = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		    Falign.o Falign_localhom.o Galign11.o SAalignmm.o Calignm1.o MSalignmm.o \
			Lalign11.o splitfromaln.o defs.o fft.o fftFunctions.o
OBJSPLITTBFAST = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		    Falign.o Falign_localhom.o Galign11.o SAalignmm.o Calignm1.o MSalignmm.o \
			Lalign11.o splittbfast.o defs.o fft.o fftFunctions.o
OBJSPLITTBFAST2 = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		    Falign.o Falign_localhom.o Galign11.o SAalignmm.o Calignm1.o MSalignmm.o \
			Lalign11.o splittbfast2.o defs.o fft.o fftFunctions.o
OBJSPLITTBFASTP = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		    Falign.o Falign_localhom.o Galign11.o SAalignmm.o Calignm1.o MSalignmm.o \
			Lalign11.o defs.o fft.o fftFunctions.o
OBJDISTTBFAST = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		    Falign.o Falign_localhom.o Galign11.o SAalignmm.o Calignm1.o MSalignmm.o \
			disttbfast.o defs.o fft.o fftFunctions.o
OBJTBFAST = mtxutl.o io.o mltaln9.o tddis.o constants.o MSalignmm.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		    Falign.o Falign_localhom.o Galign11.o SAalignmm.o Calignm1.o \
			tbfast.o defs.o fft.o fftFunctions.o
OBJTBFAST2 = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o MSalignmm.o \
		    Falign.o Falign_localhom.o Galign11.o SAalignmm.o Calignm1.o \
			tbfast2.o defs.o fft.o fftFunctions.o
OBJSETCORE = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		    Falign.o Falign_localhom.o Galign11.o SAalignmm.o Calignm1.o MSalignmm.o \
			setcore.o defs.o fft.o fftFunctions.o
OBJTDITR = mtxutl.o io.o mltaln9.o tddis.o constants.o nj.o  partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		   Calignm1.o Falign.o Falign_localhom.o Galign11.o fftFunctions.o fft.o \
		   tditeration.o tditr.o defs.o SAalignmm.o treeOperation.o
OBJDVTDITR = mtxutl.o io.o mltaln9.o tddis.o constants.o nj.o  partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
			Calignm1.o Falign.o Falign_localhom.o Galign11.o MSalignmm.o fftFunctions.o fft.o \
			tditeration.o dvtditr.o defs.o SAalignmm.o treeOperation.o
OBJGETLAG = mtxutl.o io.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
		    Falign.o Falign_localhom.o Galign11.o SAalignmm.o Calignm1.o MSalignmm.o \
			getlag.o defs.o fft.o fftFunctions.o
OBJGAPFILL = mtxutl.o io.o constants.o gapfill.o defs.o
OBJDNDFAST5 = dndfast5.o io.o constants.o mtxutl.o mltaln9.o tddis.o defs.o
OBJDNDBLAST = dndblast.o io.o constants.o mtxutl.o mltaln9.o tddis.o defs.o
OBJDNDFAST7 = dndfast7.o io.o constants.o mtxutl.o mltaln9.o tddis.o defs.o
OBJDNDFAST6 = dndfast6.o io.o constants.o mtxutl.o mltaln9.o tddis.o defs.o
OBJDNDFAST4 = dndfast4.o io.o constants.o mtxutl.o mltaln9.o tddis.o defs.o
OBJDNDFAST6 = dndfast6.o io.o constants.o mtxutl.o mltaln9.o tddis.o defs.o
OBJSEXTET5 = io.o constants.o mtxutl.o mltaln9.o tddis.o sextet5.o defs.o
OBJDISTANCE = io.o constants.o mtxutl.o mltaln9.o tddis.o mafft-distance.o defs.o
OBJTRIPLET6 = io.o constants.o mtxutl.o mltaln9.o tddis.o triplet6.o defs.o
OBJTRIPLET5 = io.o constants.o mtxutl.o mltaln9.o tddis.o triplet5.o defs.o
OBJOCTET4 = io.o constants.o mtxutl.o mltaln9.o tddis.o octet4.o defs.o
OBJDNDPRE = dndpre.o io.o constants.o mtxutl.o mltaln9.o defs.o
OBJDNDPRESCORE = dndpre2.o io.o constants.o mtxutl.o mltaln9.o defs.o
OBJGALN = io.o mtxutl.o mltaln9.o tddis.o constants.o partQalignmm.o partSalignmm.o MSalignmm.o Salignmm.o Ralignmm.o Qalignmm.o Halignmm.o \
          Calignm1.o SAalignmm.o Galign11.o Falign.o Falign_localhom.o fftFunctions.o fft.o mafft-profile.o defs.o
OBJSCORE = io.o mtxutl.o mltaln9.o score.o constants.o defs.o

HEADER = mltaln.h mtxutl.h
DPHEADER = dp.h
FFTHEADER = fft.h


#CFLAG =  -Wunused -Wreturn-type -Wshadow -pg -pedantic
#CFLAG =   -ansi -pedantic

all : $(PROGS) $(SCRIPTS)
	cp $(SCRIPTS) ../scripts
	chmod 755 ../scripts/*
	cp $(PROGS) ../binaries
	chmod 755 ../binaries/*
	@echo done.

univscript: univscript.tmpl Makefile
	sed "s:_PROGS:$(PROGS):" univscript.tmpl  > univscript

mafft: mafft.tmpl
	sed "s:_PREFIX:$(PREFIX):" mafft.tmpl  > mafft

mafft-homologs.rb: mafft-homologs.tmpl
	cp mafft-homologs.tmpl mafft-homologs.rb

mltaln.h : functions.h
	touch mltaln.h

ord : $(OBJORD)
	$(CC) -o $@ $(OBJORD) $(CFLAG) $(LIBS)

tbfast : $(OBJTBFAST)
	$(CC) -o $@ $(OBJTBFAST) $(CFLAG) $(LIBS)

tbfast2 : $(OBJTBFAST2)
	$(CC) -o $@ $(OBJTBFAST2) $(CFLAG) $(LIBS)

disttbfast : $(OBJDISTTBFAST)
	$(CC) -o $@ $(OBJDISTTBFAST) $(CFLAG) $(LIBS)

splittbfast : $(OBJSPLITTBFAST)
	$(CC) -o $@ $(OBJSPLITTBFAST) $(CFLAG) $(LIBS)

splitfromaln : $(OBJSPLITFROMALN)
	$(CC) -o $@ $(OBJSPLITFROMALN) $(CFLAG) $(LIBS)

splittbfast2 : $(OBJSPLITTBFAST2)
	$(CC) -o $@ $(OBJSPLITTBFAST2) $(CFLAG) $(LIBS)

dummy : $(OBJDUMMY)
	$(CC) -o $@ $(OBJDUMMY) $(CFLAG) $(LIBS)

setcore : $(OBJSETCORE)
	$(CC) -o $@ $(OBJSETCORE) $(CFLAG) $(LIBS)

countlen : $(OBJCOUNTLEN)
	$(CC) -o $@ $(OBJCOUNTLEN) $(CFLAG) $(LIBS)

f2cl : $(OBJF2CL)
	$(CC) -o $@ $(OBJF2CL) $(CFLAG) $(LIBS)

pairlocalalign : $(OBJPAIRLOCALALIGN)
	$(CC) -o $@ $(OBJPAIRLOCALALIGN) $(CFLAG) $(LIBS)

pair2hat3s : $(OBJPAIR2HAT3S)
	$(CC) -o $@ $(OBJPAIR2HAT3S) $(CFLAG) $(LIBS)

multi2hat3s : $(OBJMULTI2HAT3S)
	$(CC) -o $@ $(OBJMULTI2HAT3S) $(CFLAG) $(LIBS)

pairalign : $(OBJPAIRALIGN)
	$(CC) -o $@ $(OBJPAIRALIGN) $(CFLAG) $(LIBS)

getlag : $(OBJGETLAG)
	$(CC) -o $@ $(OBJGETLAG) $(CFLAG) $(LIBS)

tditr : $(OBJTDITR)
	$(CC) -o $@ $(OBJTDITR) $(CFLAG) $(LIBS)

dvtditr : $(OBJDVTDITR)
	$(CC) -o $@ $(OBJDVTDITR) $(CFLAG) $(LIBS)

mafft-profile : $(OBJGALN)
	$(CC) -o $@ $(OBJGALN) $(CFLAG) $(LIBS)

gapfill : $(OBJGAPFILL)
	$(CC) -o $@ $(OBJGAPFILL) $(CFLAG) $(LIBS)

dndfast4 : $(OBJDNDFAST4)
	$(CC) -o $@ $(OBJDNDFAST4) $(CFLAG) $(LIBS)

dndfast5 : $(OBJDNDFAST5)
	$(CC) -o $@ $(OBJDNDFAST5) $(CFLAG) $(LIBS)

dndfast6 : $(OBJDNDFAST6)
	$(CC) -o $@ $(OBJDNDFAST6) $(CFLAG) $(LIBS)

dndfast7 : $(OBJDNDFAST7)
	$(CC) -o $@ $(OBJDNDFAST7) $(CFLAG) $(LIBS)

dndblast : $(OBJDNDBLAST)
	$(CC) -o $@ $(OBJDNDBLAST) $(CFLAG) $(LIBS)

dndfast3 : $(OBJDNDFAST3)
	$(CC) -o $@ $(OBJDNDFAST3) $(CFLAG) $(LIBS)

triplet : $(OBJTRIPLET)
	$(CC) -o $@ $(OBJTRIPLET) $(CFLAG) $(LIBS)

triplet3 : $(OBJTRIPLET3)
	$(CC) -o $@ $(OBJTRIPLET3) $(CFLAG) $(LIBS)

sextet3 : $(OBJSEXTET3)
	$(CC) -o $@ $(OBJSEXTET3) $(CFLAG) $(LIBS)

sextet4 : $(OBJSEXTET4)
	$(CC) -o $@ $(OBJSEXTET4) $(CFLAG) $(LIBS)

sextet5 : $(OBJSEXTET5)
	$(CC) -o $@ $(OBJSEXTET5) $(CFLAG) $(LIBS)

mafft-distance : $(OBJDISTANCE)
	$(CC) -o $@ $(OBJDISTANCE) $(CFLAG) $(LIBS)

triplet5 : $(OBJTRIPLET5)
	$(CC) -o $@ $(OBJTRIPLET5) $(CFLAG) $(LIBS)

triplet6 : $(OBJTRIPLET6)
	$(CC) -o $@ $(OBJTRIPLET6) $(CFLAG) $(LIBS)

octet4 : $(OBJOCTET4)
	$(CC) -o $@ $(OBJOCTET4) $(CFLAG) $(LIBS)

dndpre : $(OBJDNDPRE)
	$(CC) -o $@ $(OBJDNDPRE) $(CFLAG) $(LIBS)

dndpre2 : $(OBJDNDPRESCORE)
	$(CC) -o $@ $(OBJDNDPRESCORE) $(CFLAG) $(LIBS)

score : $(OBJSCORE)
	$(CC) -o $@ $(OBJSCORE) $(CFLAG) $(LIBS)

genMtx : $(OBJGENMTX)
	$(CC) -o $@ $(OBJGENMTX) $(CFLAG) $(LIBS)

gapfill.o : gapfill.c $(HEADER)
	$(CC) $(CFLAG) -c gapfill.c

mltaln9.o : mltaln9.c $(HEADER)
	$(CC) $(CFLAG) -c mltaln9.c

tddis.o : tddis.c $(HEADER)
	$(CC) $(CFLAG) -c tddis.c

constants.o : constants.c miyata.h miyata5.h blosum.c DNA.h JTT.c $(HEADER)
	$(CC) $(CFLAG) -c constants.c

defs.o : defs.c 
	$(CC) $(CFLAG) -c defs.c

Calignm1.o : Calignm1.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c Calignm1.c

#A+++alignmm.o : SA+++alignmm.c $(HEADER) $(DPHEADER)
#	$(CC) $(CFLAG) -c SA+++alignmm.c -o A+++alignmm.o

Salignmm.o : Salignmm.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c Salignmm.c 

Halignmm.o : Halignmm.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c Halignmm.c 

Ralignmm.o : Ralignmm.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c Ralignmm.c 

Qalignmm.o : Qalignmm.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c Qalignmm.c 

MSalignmm.o : MSalignmm.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c MSalignmm.c 

partSalignmm.o : partSalignmm.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c partSalignmm.c  

partQalignmm.o : partQalignmm.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c partQalignmm.c  

Salign11.o : Salign11.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c Salign11.c -o Salign11.o

Lalign11.o : Lalign11.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c Lalign11.c 

genalign11.o : genalign11.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c genalign11.c 

suboptalign11.o : suboptalign11.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c suboptalign11.c 

VAAalign11.o : VAAalign11.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c VAAalign11.c 

Galign11.o : Galign11.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c Galign11.c 

MSalign11.o : MSalign11.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c MSalign11.c 

SAalignmm.o : SAalignmm.c $(HEADER) $(DPHEADER)
	$(CC) $(CFLAG) -c SAalignmm.c -o SAalignmm.o

ord.o : ord.c $(HEADER)
	$(CC) $(CFLAG) -c ord.c

1itr.o : 1itr.c $(HEADER)
	$(CC) $(CFLAG) -c 1itr.c

tb.o : tb.c $(HEADER)
	$(CC) $(CFLAG) -c tb.c

disttbfast.o : disttbfast.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c disttbfast.c

splitfromaln.o : splitfromaln.c $(HEADER) $(FFTHEADER) 
	$(CC) $(CFLAG) -c splitfromaln.c

splittbfast.o : splittbfast.c $(HEADER) $(FFTHEADER) 
	$(CC) $(CFLAG) -c splittbfast.c

splittbfast2.o : splittbfast2.c $(HEADER) $(FFTHEADER) 
	$(CC) $(CFLAG) -c splittbfast2.c

disttbfast_dummy.o : disttbfast_dummy.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c disttbfast_dummy.c

dummy.o : dummy.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c dummy.c

tbfast.o : tbfast.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c tbfast.c

tbfast2.o : tbfast2.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c tbfast2.c

setcore.o : setcore.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c setcore.c

getlag.o : getlag.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c getlag.c

tditr.o : tditr.c $(HEADER)
	 $(CC) $(CFLAG) -c tditr.c

dvtditr.o : dvtditr.c $(HEADER)
	 $(CC) $(CFLAG) -c dvtditr.c

tditeration.o : tditeration.c $(HEADER)
	 $(CC) $(CFLAG) -c tditeration.c

mafft-profile.o : mafft-profile.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c mafft-profile.c

dndfast4.o : dndfast4.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c dndfast4.c

dndfast5.o : dndfast5.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c dndfast5.c

dndfast6.o : dndfast6.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c dndfast6.c

dndfast7.o : dndfast7.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c dndfast7.c

dndblast.o : dndblast.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c dndblast.c

dndfast3.o : dndfast3.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c dndfast3.c

dndpre.o : dndpre.c $(HEADER)
	$(CC) $(CFLAG) -c dndpre.c

countlen.o : countlen.c $(HEADER)
	$(CC) $(CFLAG) -c countlen.c

f2cl.o : f2cl.c $(HEADER)
	$(CC) $(CFLAG) -c f2cl.c

pairlocalalign.o : pairlocalalign.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c pairlocalalign.c

multi2hat3s.o : multi2hat3s.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c multi2hat3s.c

pair2hat3s.o : pair2hat3s.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c pair2hat3s.c

pairalign.o : pairalign.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c pairalign.c

dndpre2.o : dndpre2.c $(HEADER)
	$(CC) $(CFLAG) -c dndpre2.c

io.o : io.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c io.c

nj.o : nj.c $(HEADER)
	$(CC) $(CFLAG) -c nj.c

treeOperation.o : treeOperation.c $(HEADER)
	$(CC) $(CFLAG) -c treeOperation.c

sextet5.o : sextet5.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c sextet5.c

mafft-distance.o : mafft-distance.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c mafft-distance.c

triplet5.o : triplet5.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c triplet5.c

triplet6.o : triplet6.c $(HEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c triplet6.c

fft.o : fft.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c fft.c 

fftFunctions.o : fftFunctions.c $(HEADER) $(FFTHEADER)
	$(CC) $(CFLAG) -c fftFunctions.c

Falign.o : Falign.c $(HEADER) $(FFTHEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c Falign.c

Falign_localhom.o : Falign_localhom.c $(HEADER) $(FFTHEADER) $(MTXHEADER)
	$(CC) $(CFLAG) -c Falign_localhom.c

mtxutl.o : mtxutl.c 
	$(CC) $(CFLAG) -c mtxutl.c

score.o : score.c $(HEADER)
	$(CC) $(CFLAG) -c score.c

clean :
	rm -f *.o *.a *.exe *~ $(PROGS)  $(SCRIPTS)
	rm -f ../binaries/* ../scripts/*

install : all
	mkdir -p $(PREFIX)
	chmod 755 $(PREFIX)
	mkdir -p $(PREFIX)/../../bin/
	chmod 755 $(PREFIX)/../../bin/
	chmod 755 $(SCRIPTS)
	$(INSTALL) $(SCRIPTS)  $(PREFIX)/../../bin/
	chmod 755 $(PROGS)
	$(INSTALL) $(PROGS)  $(PREFIX)/
	( cd $(PREFIX)/../../bin; \
rm -f linsi ginsi einsi fftns fftnsi nwns nwnsi ; \
rm -f mafft-linsi mafft-ginsi mafft-einsi mafft-fftns mafft-fftnsi mafft-nwns mafft-nwnsi ; \
ln -s mafft linsi; ln -s mafft ginsi; ln -s mafft fftns; \
ln -s mafft fftnsi; ln -s mafft nwns; ln -s mafft nwnsi; \
ln -s mafft einsi; \
ln -s mafft mafft-linsi; ln -s mafft mafft-ginsi; ln -s mafft mafft-fftns; \
ln -s mafft mafft-fftnsi; ln -s mafft mafft-nwns; ln -s mafft mafft-nwnsi; \
ln -s mafft mafft-einsi; \
rm -f mafft-profile mafft-profile.exe; ln -s ../lib/mafft/mafft-profile .; \
rm -f mafft-distance mafft-distance.exe; ln -s ../lib/mafft/mafft-distance . )
