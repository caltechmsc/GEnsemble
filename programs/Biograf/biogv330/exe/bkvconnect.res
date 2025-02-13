**********************************************************************
* Data file for generating connectivity information of residues 
* in Brookhaven Data Base.
*
* Different terminal groups are also included at the end.  
*                                                      (ms 9/9/87)
*
* -------------------------------------------------------------------- 
* NOTES:
*  
*  1.  This residue file does not contain any information about hydrogens
*      ( deuteriums) present in common ribonucleotides (A,G,C,U,T) and
*      about non standard groups (HEM,NAD,NADP).  Consequently no 
*      implicit connectivity information will be generated about these
*      atoms.
*              
*      This can be fixed by checking the format for representing these
*      hydrogens in a Brookhaven Data Bank file (neuotron diffraction
*      or protein data) and putting the data in this file.
*
*  2.  Hydrogens representation in Kollman's format has also been added
*      for each residue (to read Kollman's files properly).  
*
*  3.  Non-standard residues (used frequently in Kollman's data files) like
*      QNX,NCY etc. have also been added.
*
*  4.  Added different kinds of HISTIDINE (HIS,HID,HIP,HIE,HSD,HSP).
*
* ---------------------------------------------------------------------
* RESIDUE NAME FORMAT
*     
*        Cols.  1-7     RESIDUE
*              10-12    Residue name
*
*        Fortran format:  A7,2x,A3
*
* DATA LINE FOR A GIVEN RESIDUE
* 
*        Cols.  1-5      Central atom
*               6-10     Connected atom
*               11       Bond order of connected atom
*               13-17    Connected atom
*               18       Bond order of connected atom
*               .. ..
*               .. ..
*               .. ..
*
*
*    Fortran format
*
*       A5,8(A5,I1,1X)
*
*   Notes. 1.     Bond order         Type of bond
*                 ----------         ------------        
*                     0               Single (or none) 
*                     2               Double
*                     3               Triple 
*
*          2.'*' separates one residue from the other and is also used for
*             writing commented lines.
*
*          3. '#' is used as a wild card.It will match blank or any number
*              from 1 to 9.
*
*          4. Maximum number of connected atoms allowed is six.
*
*          5. '-' and '+' in atom names indicate atom of previous or forward
*             residue in peptide chain to which that particular atom should
*             be connected (if any).
*
*  
**************************************************************************
RESIDUE	 ALA
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA    HB1    HB2    HB3    #HB    #DB
 OXT  C
#H    N
#D    N
HN   N
 HA   CA
 DA   CA
#HB   CB
#DB   CB
HB1   CB
HB2   CB
HB3   CB   
*
RESIDUE  SER 
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     OG    #HB    #DB    HB1    HB2
 OG   CB     HG     DG    HOG
 OXT  C
#H    N
#D    N 
HN    N
 HA   CA
 DA   CA
#HB   CB
#DB   CB
HB1   CB
HB2   CB
 HG   OG
 DG   OG
HOG   OG  
*     
*O-BRIDGED SERINE 
*for Kollman residue
RESIDUE  SEO
 N    CA    -C     #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     OG    #HB    #DB    HB1    HB2
 OG   CB    
 OXT  C
#H    N
#D    N 
HN    N
 HA   CA
 DA   CA
#HB   CB
#DB   CB
HB1   CB
HB2   CB
*
RESIDUE  GLY
 N   -C      CA    HN     #H     #D
 CA   N      C     HA1    HA2    #HA    #DA  
 C    CA     O   2  OXT   +N
 O    C   2
 OXT  C
HN    N
#H    N 
#D    N
#HA   CA
#DA   CA 
HA1   CA
HA2   CA 
*
RESIDUE  LEU
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     CD1    CD2    HG     DG 
 CD1  CG    #HD1   #DD1   HD1    HD2    HD3
 CD2  CG    #HD2   #DD2   HD4    HD5    HD6
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA
#HB   CB
#DB   CB 
HB1   CB
HB2   CB 
 HG   CG
 DG   CG
#HD1  CD1 
#DD1  CD1
HD1   CD1
HD2   CD2
HD3   CD3
#HD2  CD2
#DD2  CD2
HD4   CD2
HD5   CD2
HD6   CD2  
*
RESIDUE  LYS
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     CD    #HG    #DG    HG1    HG2
 CD   CG     CE    #HD    #DD    HD1    HD2
 CE   CD     NZ    #HE    #DE    HE1    HE2
 NZ   CE    #HZ    #DZ    HNZ1   HNZ2   HNZ3
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB
HB1   CB
HB2   CB
#HG   CG
#DG   CG
HG1   CG
HG2   CG
#HD   CD 
#DD   CD
HD1   CD
HD2   CD
#HE   CE
#DE   CE
HE1   CE
HE2   CE
#HZ   NZ
#DZ   NZ
HNZ1  NZ
HNZ2  NZ
HNZ3  NZ 
*
RESIDUE  VAL
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG1    CG2   #HB    #DB     HB
 CG1  CB    #HG1   #DG1   HG1    HG2    HG3
 CG2  CB    #HG2   #DG2   HG4    HG5    HG6
 OXT  C 
#H    N  
#D    N 
HN    N
 HA   CA
 DA   CA
#HB   CB
#DB   CB
 HB   CB
#HG1  CG1
#DG1  CG1
HG1   CG1
HG2   CG1
HG3   CG1
#HG2  CG2
#DG2  CG2
HG4   CG2
HG5   CG2
HG6   CG2   
*
* for kollman residue.  
* N-METHYL VALINE
RESIDUE  NMV
 N   -C      CA     CN    #H     #D     HN
 CN   N     HCN1   HCN2   HCN3   HK1    HK2    HK3  
HCN1  CN
HCN2  CN
HCN3  CN                                
HK1   CN
HK2   CN
HK3   CN                                
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N 
 O    C   2 
 CB   CA     CG1    CG2   #HB    #DB     HB
 CG1  CB    #HG1   #DG1   HG1    HG2    HG3
 CG2  CB    #HG2   #DG2   HG4    HG5    HG6
 OXT  C 
#H    N  
#D    N 
HN    N
 HA   CA
 DA   CA
#HB   CB
#DB   CB
 HB   CB
#HG1  CG1
#DG1  CG1
HG1   CG1
HG2   CG1
HG3   CG1
#HG2  CG2
#DG2  CG2
HG4   CG2
HG5   CG2
HG6   CG2   
*
* Kollman residue
* Quinoxaline
RESIDUE  QNX
 C9  HC9     N3     C2
 N3   C9     C8
 C8   N3     C3
 C7  HC7     C6     C8
 C6   C5     C7     HC6 
 C5   C4    HC5     C6
 C4   C3    HC4     C5
 C3   C8     C4     N2
 N2   C3     C2
 C2   C9     N2     C1
 C1   C2     O1  2 +N
 O1   C1  2
HC9   C9
HC7   C7
HC6   C6
HC5   C5
HC4   C4
*
RESIDUE  THR
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     OG1    CG2   #HB    #DB     HB
 OG1  CB    #HG1   #DG1   HOG
 CG2  CB    #HG2   #DG2   HG1    HG2    HG3
 OXT  C
#H    N  
#D    N 
HN    N
 HA   CA
 DA   CA 
#HB   CB 
#DB   CB
 HB   CB
#HG1  OG1
#DG1  OG1
HOG   OG1
#HG2  CG2
#DG2  CG2
HG1   CG2
HG2   CG2
HG3   CG2  
*
RESIDUE  PRO                            
 N   -C      CA     CD    #H     #D     HN
 CA   N      C      CB     HA     DA   
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     CD    #HG    #DG    HG1    HG2
 CD   N      CG    #HD    #DD    HD1    HD2
 OXT  C 
#H    N  
#D    N 
HN    N
 HA   CA
 DA   CA 
#HB   CB
#DB   CB
HB1   CB
HB2   CB
#HG   CG
#DG   CG
HG1   CG
HG2   CG
#HD   CD
#DD   CD
HD1   CD
HD2   CD 
*
RESIDUE  ASP
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     OD1 2  OD2    HG     DG 
 OD1  CG  2  HD1    DD1 
 OD2  CG     HD2    DD2 
 OXT  C 
#H    N  
#D    N 
HN    N
 HA   CA
 DA   CA  
#HB   CB
#DB   CB
HB1   CB
HB2   CB
 HG   CG
 DG   CG
 HD1  OD1
 DD1  OD1
 HD2  OD2
 DD2  OD2
*
RESIDUE  GLU
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     CD    #HG    #DG    HG1    HG2
 CD   CG     OE1 2  OE2    HD     DD 
 OE1  CD  2  HE1    DE1   
 OE2  CD     HE2    DE2 
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB
HB1   CB
HB2   CB 
#HG   CG
#DG   CG 
HG1   CG
HG2   CG
 HD   CD
 DD   CD
 HE1  OE1
 DE1  OE1
 HE2  OE2
 DE2  OE2 
*
RESIDUE  ILE 
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG1    CG2    HB     DB 
 CG1  CB     CD1   #HG1   #DG1   HG4    HG5
 CG2  CB    #HG2   #DG2   HG1    HG2    HG3
 CD1  CG1   #HD1   #DD1   HD1    HD2    HD3
 OXT  C 
#H    N  
#D    N   
HN   N
 HA   CA
 DA   CA
 HB   CB
 DB   CB 
#HG1  CG1
#DG1  CG1
HG4  CG1
HG5  CG1
#HG2  CG2
#DG2  CG2
HG1  CG2
HG2  CG2
HG3  CG2
#HD1  CD1
#DD1  CD1
HD1  CD1
HD2  CD1
HD3  CD1 
*
RESIDUE  ASN
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     OD1 2  ND2    AD1    AD2    HG     DG  
 OD1  CG  2  
 ND2  CG    #HD2   #DD2   HND1   HND2
 AD1  CG
 AD2  CG
 OXT  C
#H    N  
#D    N  
HN    N
 HA   CA
 DA   CA
 HG   CG 
 DG   CG  
#HB   CB
#DB   CB
HB1   CB
HB2   CB
#HD2  ND2
#DD2  ND2
HND1  ND2
HND2  ND2 
*
RESIDUE  ARG 
 N   -C      CA    #H     #D     HN                
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     CD    #HG    #DG    HG1    HG2
 CD   CG     NE    #HD    #DD    HD1    HD2
 NE   CD     CZ    #HE    #DE    HNE
 CZ   NE     NH1    NH2 2  HZ     DZ  
 NH1  CZ    #HH1   #DH1   HN11   HN12
 NH2  CZ  2 #HH2   #DH2   HN21   HN22
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB
HB1   CB
HB2   CB
#HG   CG
#DG   CG 
HG1   CG
HG2   CG
#HD   CD
#DD   CD
HD1   CD
HD2   CD
#HE   NE
#DE   NE
HNE   NE
 HZ   CZ
 DZ   CZ 
#HH1  NH1
#DH1  NH1
HN11  NH1
HN12  NH1
#HH2  NH2
#DH2  NH2
HN21  NH2
HN22  NH2 
*     
RESIDUE  GLN      
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     CD    #HG    #DG    HG1    HG2
 CD   CG     OE1 2  NE2    AE1    AE2    HD     DD      
 OE1  CD  2   
 NE2  CD    #HE2   #DE2   HNE1   HNE2
 AE1  CD
 AE2  CD
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB
HB1   CB
HB2   CB
#HG   CG
#DG   CG
HG1   CG
HG2   CG
 HD   CD
 DD   CD  
#HE2  NE2
#DE2  NE2
HNE1  NE2
HNE2  NE2  
*
RESIDUE  PHE
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     CD1 2  CD2   
 CD1  CG  2  CE1    HD1    DD1    
 CD2  CG     CE2 2  HD2    DD2    
 CE1  CD1    CZ  2  HE1    DE1  
 CE2  CD2 2  CZ     HE2    DE2 
 CZ   CE1 2  CE2    HZ     DZ    HZ1
 OXT  C
#H    N  
#D    N 
HN    N
 HA   CA
 DA   CA 
#HB   CB
#DB   CB 
HB1   CB
HB2   CB
 HD1  CD1
 DD1  CD1
 HD2  CD2
 DD2  CD2 
 HE1  CE1 
 DE1  CE1
 HE2  CE2
 DE2  CE2
 HZ   CZ
 DZ   CZ 
HZ1   CZ 
*
RESIDUE  TYR 
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     CD1 2  CD2
 CD1  CG  2  CE1    HD1    DD1 
 CD2  CG     CE2 2  HD2    DD2  
 CE1  CD1    CZ  2  HE1    DE1  
 CE2  CD2 2  CZ     HE2    DE2 
 CZ   CE1 2  CE2    OH
 OH   CZ     HH     DH    HOH
 OXT  C 
#H    N  
#D    N 
HN    N
 HA   CA
 DA   CA 
#HB   CB
#DB   CB
HB1   CB
HB2   CB
 HD1  CD1
 DD1  CD1
 HD2  CD2
 DD2  CD2 
 HE1  CE1
 DE1  CE1
 HE2  CE2
 DE2  CE2
 HH   OH
 DH   OH 
HOH   OH
*
RESIDUE  CYS              
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     SG    #HB    #DB    HB1    HB2
 SG   CB     HG    HSG    DG     LP1    LP2
 OXT  C
#H    N     
#D    N 
HN    N
 HA   CA
 DA   CA 
#HB   CB
#DB   CB 
HB1   CB
HB2   CB
 HG   SG
 DG   SG
HSG   SG 
LP1   SG
LP2   SG
*       
* N-methyl cystine
* Kollman residue
RESIDUE  NCY     
 N   -C      CA     CN    #H     #D     HN 
 CN   N     HCN1   HCN2   HCN3   HK1    HK2    HK3
HCN1  CN
HCN2  CN
HCN3  CN
HK1   CN
HK2   CN
HK3   CN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     SG    #HB    #DB    HB1    HB2
 SG   CB     HG    HSG    LP1    LP2
 OXT  C
#H    N     
#D    N 
HN    N
 HA   CA
 DA   CA 
#HB   CB
#DB   CB 
HB1   CB
HB2   CB
 HG   SG
HSG   SG 
LP1   SG
LP2   SG
*
RESIDUE  CYX              
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     SG    #HB    #DB    HB1    HB2
 SG   CB    LP1    LP2
 OXT  C
#H    N     
#D    N 
HN    N
 HA   CA
 DA   CA 
#HB   CB
#DB   CB 
HB1   CB
HB2   CB
LP1   SG
LP2   SG
*
RESIDUE  HIS
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     ND1    CD2 2  AD1    AD2
 ND1  CG     CE1    AE1    HD1    DD1   HND
 CD2  CG  2  NE2    AE2    HD2    DD2   HD
 CE1  ND1    AD1    NE2 2  AE2    HE1    DE1   HE
 NE2  CD2    AD2    CE1 2  AE1    HE2    DE2   HNE
 AD1  CG     CE1    AE1
 AD2  CG     NE2    AE2
 AE1  ND1    AD1    NE2    AE2
 AE2  CD2    AD2    CE1    AE1
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB 
HB1   CB
HB2   CB
 HD1  ND1
 DD1  ND1
HND   ND1
 HD2  CD2
 DD2  CD2
HD    CD2
 HE1  CE1
 DE1  CE1
HE    CE1
 HE2  NE2
 DE2  NE2
HNE   NE2  
*
RESIDUE  HIP
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     ND1    CD2 2 
 ND1  CG     CE1    HD1    DD1   HND
 CD2  CG  2  NE2    HD2    DD2   HD
 CE1  ND1    NE2    HE1    DE1   HE
 NE2  CD2    CE1    HE2    DE2   HNE
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB 
HB1   CB
HB2   CB
 HD1  ND1
 DD1  ND1
HND   ND1
 HD2  CD2
 DD2  CD2
HD    CD2
 HE1  CE1
 DE1  CE1
HE    CE1
 HE2  NE2
 DE2  NE2
HNE   NE2
*  
RESIDUE  HIE
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     ND1    CD2 2 
 ND1  CG     CE1  
 CD2  CG  2  NE2    HD2    DD2   HD
 CE1  ND1    NE2    HE1    DE1   HE
 NE2  CD2    CE1    HE2    DE2   HNE
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB 
HB1   CB
HB2   CB
 HD2  CD2
 DD2  CD2
HD    CD2
 HE1  CE1
 DE1  CE1
HE    CE1
 HE2  NE2
 DE2  NE2
HNE   NE2  
*  
RESIDUE  HSD
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     ND1    CD2 2 
 ND1  CG     CE1  
 CD2  CG  2  NE2    HD2    DD2   HD
 CE1  ND1    NE2    HE1    DE1   HE
 NE2  CD2    CE1    HE2    DE2   HNE
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB 
HB1   CB
HB2   CB
 HD2  CD2
 DD2  CD2
HD    CD2
 HE1  CE1
 DE1  CE1
HE    CE1
 HE2  NE2
 DE2  NE2
HNE   NE2  
*
RESIDUE  HID
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     ND1    CD2 2 
 ND1  CG     CE1    HD1    DD1   HND
 CD2  CG  2  NE2    HD2    DD2   HD
 CE1  ND1    NE2    HE1    DE1   HE
 NE2  CD2    CE1  
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB 
HB1   CB
HB2   CB
 HD1  ND1
 DD1  ND1
HND   ND1
 HD2  CD2
 DD2  CD2
HD    CD2
 HE1  CE1
 DE1  CE1
HE    CE1
*
RESIDUE  HSP
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     ND1    CD2 2 
 ND1  CG     CE1    HD1    DD1   HND
 CD2  CG  2  NE2    HD2    DD2   HD
 CE1  ND1    NE2    HE1    DE1   HE
 NE2  CD2    CE1  
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB 
HB1   CB
HB2   CB
 HD1  ND1
 DD1  ND1
HND   ND1
 HD2  CD2
 DD2  CD2
HD    CD2
 HE1  CE1
 DE1  CE1
HE    CE1
*
RESIDUE  MET   
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CB     SD    #HG    #DG    HG1    HG2
 SD   CG     CE    LP1    LP2
 CE   SD    #HE    #DE    HE1    HE2    HE3
 OXT  C
#H    N  
#D    N 
HN    N
 HA   CA
 DA   CA 
#HB   CB
#DB   CB
HB1   CB
HB2   CB 
#HG   CG
#DG   CG
HG1   CG
HG2   CG 
LP1   SD
LP2   SD
#HE   CE
#DE   CE
HE1   CE
HE2   CE 
HE3   CE 
*
RESIDUE  TRP 
 N   -C      CA    #H     #D     HN
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB    HB1    HB2
 CG   CD1 2  CD2
 CD1  CG  2  NE1   #HD1   #DD1   HD
 CD2  CG     CE2 2  CE3
 NE1  CD1    CE2   #HE1   #DE1   HNE
 CE2  CD2 2  NE1    CZ2
 CE3  CD2    CZ3 2 #HE3   #DE3   HE
 CZ2  CE2    CH2 2 #HZ2   #DZ2   HZ1
 CZ3  CE3 2  CH2   #HZ3   #DZ3   HZ2
 CH2  CZ2 2  CZ3   #HH2   #DH2   HH
 OXT  C
#H    N  
#D    N
HN    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB
HB1   CB
HB2   CB
#HD1  CD1
#DD1  CD1
HD    CD1
#HE1  NE1
#DE1  NE1  
HNE   NE1
#HE3  CE3 
#DE3  CE3 
HE    CE3
#HZ2  CZ2
#DZ2  CZ2
HZ1   CZ2 
#HZ3  CZ3
#DZ3  CZ3 
HZ2   CZ3
#HH2  CH2 
#DH2  CH2
HH    CH2  
*
RESIDUE  GLX 
 N   -C      CA    #H     #D  
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB 
 CG   CB     CD    #HG    #DG 
 CD   CG     AE1    AE2    HD     DD  
 AE1  CD
 AE2  CD
 OXT  C
#H    N  
#D    N 
 HA   CA
 DA   CA
#HB   CB
#DB   CB
#HG   CG
#DG   CG  
 HD   CD
 DD   CD 
*
RESIDUE  ASX
 N   -C      CA    #H     #D  
 CA   N      C      CB     HA     DA  
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB 
 CG   CB     AD1    AD2    HG     DG 
 AD1  CG
 AD2  CG
 OXT  C
#H    N  
#D    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB
 HG   CG
 DG   CG  
*
RESIDUE  PCA 
 N   -C      CA     CD    #H     #D    
 CA   N      C      CB     HA     DA   
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA     CG    #HB    #DB 
 CG   CB     CD    #HG    #DG 
 CD   N      CG     OE  2 
 OE   CD  2
 OXT  C
#H    N  
#D    N 
 HA   CA
 DA   CA 
#HB   CB
#DB   CB
#HG   CG
#DG   CG  
*
RESIDUE  UNK
 N   -C      CA    
 CA   N      C      CB
 C    CA     O   2  OXT   +N
 O    C   2 
 CB   CA    
 OXT  C
*
RESIDUE  HEM
FE    N A    N B    N C    N D    OH2 
 CHA  C1A 2  C4D
 CHB  C4A 2  C1B
 CHC  C4B 2  C1C
 CHD  C4C    C1D 2  
 N A FE      C1A    C4A
 C1A  CHA 2  N A    C2A
 C2A  C1A    C3A 2  CAA
 C3A  C2A 2  C4A    CMA
 C4A  CHB 2  N A    C3A
 CMA  C3A
 CAA  C2A    CBA
 CBA  CAA    CGA
 CGA  CBA    O1A 2  O2A
 O1A  CGA 2  
 O2A  CGA
 N B FE      C1B 2  C4B
 C1B  CHB    N B 2  C2B
 C2B  C1B    C3B 2  CMB
 C3B  C2B 2  C4B    CAB
 C4B  CHC 2  N B    C3B
 CMB  C2B
 CAB  C3B    CBB 2  
 CBB  CAB 2  
 N C FE      C1C    C4C
 C1C  CHC    N C    C2C 2  
 C2C  C1C 2  C3C    CMC
 C3C  C2C    C4C 2  CAC
 C4C  CHD    N C    C3C 2 
 CMC  C2C
 CAC  C3C    CBC 2  
 CBC  CAC 2  
 N D FE      C1D    C4D 2  
 C1D  CHD 2  N D    C2D
 C2D  C1D    C3D 2  CMD
 C3D  C2D 2  C4D    CAD
 C4D  CHA    N D 2  C3D
 CMD  C2D
 CAD  C3D    CBD
 CBD  CAD    CGD
 CGD  CBD    O1D 2  O2D
 O1D  CGD 2   
 O2D  CGD
 OH2 FE
*
RESIDUE  NAD 
AP   AO1    AO2    AO5*    O3
AO1  AP
AO2  AP
AO5* AP     AC5*
AC5* AO5*   AC4*
AC4* AC5*   AO4*   AC3*
AO4* AC4*   AC1*   
AC3* AC4*   AO3*   AC2*
AO3* AC3*   
AC2* AC3*   AO2*   AC1*
AO2* AC2*
AC1* AO4*   AC2*   AN9
AN9  AC1*   AC8    AC4
AC8  AN9    AN7
AN7  AC8    AC5
AC5  AN7    AC6    AC4
AC6  AC5    AN6    AN1
AN6  AC6
AN1  AC6    AC2
AC2  AN1    AN3
AN3  AC2    AC4
AC4  AN9    AC5    AN3
 O3  AP     NP
NP    O3    NO1    NO2    NO5*
NO1  NP
NO2  NP
NO5* NP     NC5*
NC5* NO5*   NC4*
NC4* NC5*   NO4*   NC3*
NO4* NC4*   NC1*
NC3* NC4*   NO3*   NC2*
NO3* NC3*   
NC2* NC3*   NO2*   NC1*
NO2* NC2* 
NC1* NO4*   NC2*   NN1
NN1  NC1*   NC2    NC6
NC2  NN1    NC3
NC3  NC2    NC7    NC4
NC7  NC3    NO7    NN7  
NO7  NC7
NN7  NC7 
NC4  NC3    NC5
NC5  NC4    NC6
NC6  NN1    NC5
*
RESIDUE    A 
 OXT  P
 P   -O3*    OXT    O1P 2  O2P    O5*
 O1P  P   2
 O2P  P
 O5*  P      C5*
 C5*  O5*    C4*
 C4*  C5*    O4*    C3*
 O4*  C4*    C1*
 C3*  C4*    O3*    C2*
 O3*  C3*   +P 
 C2*  C3*    O2*    C1*
 O2*  C2*    
 C1*  O4*    C2*    N9
 N9   C1*    C8     C4
 C8   N9     N7  2       
 N7   C8  2  C5
 C5   N7     C6     C4  2  
 C6   C5     N6     N1  2
 N6   C6       
 N1   C6  2  C2 
 C2   N1     N3  2    
 N3   C2  2  C4
 C4   N9     C5  2  N3     
*
RESIDUE    I 
 OXT  P
 P   -O3*    OXT    O1P 2  O2P    O5*
 O1P  P   2
 O2P  P
 O5*  P      C5*
 C5*  O5*    C4*
 C4*  C5*    O4*    C3*
 O4*  C4*    C1*
 C3*  C4*    O3*    C2*
 O3*  C3*   +P 
 C2*  C3*    O2*    C1*
 O2*  C2*    
 C1*  O4*    C2*    N9
 N9   C1*    C8     C4
 C8   N9     N7  2       
 N7   C8  2  C5
 C5   N7     C6     C4  2  
 C6   C5     O6  2  N1   
 O6   C6  2    
 N1   C6     C2 
 C2   N1     N3  2    
 N3   C2  2  C4
 C4   N9     C5  2  N3     
*
RESIDUE    G 
 OXT  P
 P   -O3*    OXT    O1P 2  O2P    O5*
 O1P  P   2
 O2P  P
 O5*  P      C5*
 C5*  O5*    C4*
 C4*  C5*    O4*    C3*
 O4*  C4*    C1*
 C3*  C4*    O3*    C2*
 O3*  C3*   +P 
 C2*  C3*    O2*    C1*
 O2*  C2*    
 C1*  O4*    C2*    N9
 N9   C1*    C8     C4
 C8   N9     N7  2  
 N7   C8  2  C5  
 C5   N7     C6     C4  2   
 C6   C5     O6  2  N1
 O6   C6  2   
 N1   C6     C2 
 C2   N1     N2     N3  2  
 N2   C3 
 N3   C2  2  C4
 C4   N9     C5  2  N3    
*
RESIDUE    C 
 OXT  P
 P   -O3*    OXT    O1P 2  O2P    O5*
 O1P  P   2
 O2P  P
 O5*  P      C5* 
 C5*  O5*    C4*    
 C4*  C5*    O4*    C3*
 O4*  C4*    C1*
 C3*  C4*    O3*    C2*
 O3*  C3*   +P     
 C2*  C3*    O2*    C1*
 O2*  C2*    
 C1*  O4*    C2*    N1
 N1   C1*    C2     C6
 C2   N1     O2  2  N3
 O2   C2  2   
 N3   C2     C4  2       
 C4   N3  2  N4     C5
 N4   C4
 C5   C4     C6  2
 C6   N1     C5  2  
*
RESIDUE    U 
 OXT  P
 P   -O3*    OXT    O1P 2  O2P    O5*
 O1P  P   2
 O2P  P
 O5*  P      C5* 
 C5*  O5*    C4*    
 C4*  C5*    O4*    C3*
 O4*  C4*    C1*
 C3*  C4*    O3*    C2*
 O3*  C3*   +P     
 C2*  C3*    O2*    C1*
 O2*  C2*    
 C1*  O4*    C2*    N1
 N1   C1*    C2     C6
 C2   N1     O2  2  N3
 O2   C2  2  
 N3   C2     C4     
 C4   N3     O4  2  C5
 O4   C4  2  
 C5   C4     C6  2
 C6   N1     C5  2  
*
RESIDUE    T 
 OXT  P
 P   -O3*    OXT    O1P 2  O2P    O5*
 O1P  P   2
 O2P  P
 O5*  P      C5* 
 C5*  O5*    C4*    
 C4*  C5*    O4*    C3*
 O4*  C4*    C1*
 C3*  C4*    O3*    C2*
 O3*  C3*   +P     
 C2*  C3*    O2*    C1*
 O2*  C2*    
 C1*  O4*    C2*    N1
 N1   C1*    C2     C6
 C2   N1     O2  2  N3
 O2   C2  2  
 N3   C2     C4     
 C4   N3     O4  2  C5
 O4   C4  2  
 C5   C4     C6  2  C5M
 C5M  C5
 C6   N1     C5  2  
*
RESIDUE  5MU 
 OXT  P
 P   -O3*    OXT    O1P 2  O2P    O5*
 O1P  P   2
 O2P  P
 O5*  P      C5* 
 C5*  O5*    C4*    
 C4*  C5*    O4*    C3*
 O4*  C4*    C1*
 C3*  C4*    O3*    C2*
 O3*  C3*   +P     
 C2*  C3*    O2*    C1*
 O2*  C2*    
 C1*  O4*    C2*    N1
 N1   C1*    C2     C6
 C2   N1     O2  2  N3
 O2   C2  2  
 N3   C2     C4     
 C4   N3     O4  2  C5
 O4   C4  2  
 C5   C4     C6  2  C5M
 C5M  C5
 C6   N1     C5  2  
*
*  Kollman's residues (ADE,THY,URA,GUA,CYT) used for nucleotides have
*    a representation format quite different from standard Brookhaven
*    format.
*
RESIDUE  ADE 
O5'  C5'    -H     -P
C5'  O5'    H5A'   H5B'   C4'   
H5A' C5'
H5B' C5'
C4'  H4'    O1'    C3'    C5'  
H4'  C4'
O1'  C4'    C1'
C1'  O1'    C2'    H1'    N9
H1'  C1'
C3'  C2'    C4'    O3'    H3'
H3'  C3'
C2'  C1'    C3'    O2'    H2A'   H2B'
H2A' C2'
H2B' C2'
O2'  C2'    HO2'   
O3'  C3'    +P     +H
N9   C1'    C8     C4
C8   N9     N7   2 H8
H8   C8     
N7   C8   2 C5
C5   N7     C6     C4   2  
C6   C5     N6     N1   2
N6   C6     HN6A   HN6B
HN6A N6
HN6B N6  
N1   C6   2 C2 
C2   N1     N3   2 H2
H2   C2  
N3   C2   2 C4
C4   N9     C5   2 N3     
*
RESIDUE  GUA 
O5'  C5'    -H     -P
C5'  O5'    H5A'   H5B'   C4'   
H5A' C5'
H5B' C5'
C4'  H4'    O1'    C3'    C5'  
H4'  C4'
O1'  C4'    C1'
C1'  O1'    C2'    H1'    N9
H1'  C1'
C3'  C2'    C4'    O3'    H3'
H3'  C3'
C2'  C1'    C3'    O2'    H2A'   H2B'
H2A' C2'
H2B' C2'
O2'  C2'    HO2'   
O3'  C3'    +P     +H
N9   C1'    C8     C4
C8   N9     N7   2 H8
H8   C8 
N7   C8   2 C5  
C5   N7     C6     C4   2   
C6   C5     O6   2 N1
O6   C6   2   
N1   C6     C2     H1
H1   N1
C2   N1     N2     N3   2  
N2   C3     HN2A   HN2B
HN2A N2
HN2B N2
N3   C2   2 C4
C4   N9     C5   2 N3    
*
RESIDUE  CYT   
O5'  C5'    -H     -P
C5'  O5'    H5A'   H5B'   C4'   
H5A' C5'
H5B' C5'
C4'  H4'    O1'    C3'    C5'  
H4'  C4'
O1'  C4'    C1'
C1'  O1'    C2'    H1'    N1
H1'  C1'
C3'  C2'    C4'    O3'    H3'
H3'  C3'
C2'  C1'    C3'    O2'    H2A'   H2B'
H2A' C2'
H2B' C2'
O2'  C2'    HO2'   
O3'  C3'    +P     +H
N1   C1'    C2     C6
C2   N1     O2   2 N3
O2   C2   2   
N3   C2     C4   2       
C4   N3   2 N4     C5
N4   C4     HN4A   HN4B
HN4A N4
HN4B N4
C5   C4     C6   2 H5
H5   C5
C6   N1     C5   2 H6
H6   C6 
*
RESIDUE  URA 
O5'  C5'    -H     -P
C5'  O5'    H5A'   H5B'   C4'   
H5A' C5'
H5B' C5'
C4'  H4'    O1'    C3'    C5'  
H4'  C4'
O1'  C4'    C1'
C1'  O1'    C2'    H1'    N1
H1'  C1'
C3'  C2'    C4'    O3'    H3'
H3'  C3'
C2'  C1'    C3'    O2'    H2A'   H2B'
H2A' C2'
H2B' C2'
O2'  C2'    HO2'   
O3'  C3'    +P     +H
N1   C1'    C2     C6
C2   N1     O2   2 N3
O2   C2   2  
N3   C2     C4     H3
H3   N3
C4   N3     O4   2 C5
O4   C4   2  
C5   C4     C6   2 H5
C6   N1     C5   2 H6
H6   C6 
*
RESIDUE  THY 
O5'  C5'    -H     -P
C5'  O5'    H5A'   H5B'   C4'   
H5A' C5'
H5B' C5'
C4'  H4'    O1'    C3'    C5'  
H4'  C4'
O1'  C4'    C1'
C1'  O1'    C2'    H1'    N1
H1'  C1'
C3'  C2'    C4'    O3'    H3'
H3'  C3'
C2'  C1'    C3'    O2'    H2A'   H2B'
H2A' C2'
H2B' C2'
O2'  C2'    HO2'   
O3'  C3'    +P     +H
N1   C1'    C2     C6
C2   N1     O2   2 N3
O2   C2   2  
N3   C2     C4     H3
H3   N3
C4   N3     O4   2 C5
O4   C4   2  
C5   C4     C6   2 C7
C7   C5     H7A    H7B    H7C
H7A  C7
H7B  C7
H7C  C7
C6   N1     C5   2 H6
H6   C6 
*      
* 0H BEGINING   ?
RESIDUE  OHB
O    +C4'   H
H    O
*  OH END
RESIDUE  OHE     ?
O    -C5'   H
H    O 
*  H BEGINING 
RESIDUE  HB
H    +O5'
*  H END
RESIDUE  HE
H    -O3'
* 
RESIDUE  POM 
P    OA     OB     -O3'   +O5'
OA   P
OB   P
*
RESIDUE  5MU 
 OXT  P
 P   -O3*    OXT    O1P 2  O2P    O5*
 O1P  P   2
 O2P  P
 O5*  P      C5* 
 C5*  O5*    C4*    
 C4*  C5*    O4*    C3*
 O4*  C4*    C1*
 C3*  C4*    O3*    C2*
 O3*  C3*   +P     
 C2*  C3*    O2*    C1*
 O2*  C2*    
 C1*  O4*    C2*    N1
 N1   C1*    C2     C6
 C2   N1     O2  2  N3
 O2   C2  2  
 N3   C2     C4     
 C4   N3     O4  2  C5
 O4   C4  2  
 C5   C4     C6  2  C5M
 C5M  C5
 C6   N1     C5  2  
*
RESIDUE  PSU 
 OXT  P
 P   -O3*    OXT    O1P 2  O2P    O5*
 O1P  P   2
 O2P  P
 O5*  P      C5*
 C5*  O5*    C4*
 C4*  C5*    O4*    C3*
 O4*  C4*    C1*
 C3*  C4*    O3*    C2*
 O3*  C3*   +P 
 C2*  C3*    O2*    C1*
 O2*  C2*
 C1*  O4*    C2*    C5
 N1   C2     C6
 C2   N1     O2  2  N3
 O2   C2  2  
 N3   C2     C4
 C4   N3     O4  2  C5
 O4   C4  2  
 C5   C1*    C4     C6  2
 C6   N1     C5  2  
*
RESIDUE  M2G 
 OXT  P
 P   -O3*    OXT    O1P 2  O2P    O5*
 O1P  P   2
 O2P  P
 O5*  P      C5*
 C5*  O5*    C4*
 C4*  C5*    O4*    C3*
 O4*  C4*    C1*
 C3*  C4*    O3*    C2*
 O3*  C3*   +P   
 C2*  C3*    O2*    C1*
 O2*  C2*
 C1*  O4*    C2*    N9
 N9   C1*    C8     C4
 C8   N9     N7  2  
 N7   C8  2  C5
 C5   N7     C6     C4  2
 C6   C5     O6  2  N1
 O6   C6  2  
 N1   C6     C2
 C2   N1     N2     N3  2  
 N2   C2     C2A    C2B 
 C2A  N2
 C2B  N2
 N3   C2  2  C4
 C4   N9     C5  2  N3
*
*
* -----------------------------------------------------------
* Data for different terminal groups             
*
RESIDUE  ACE
 C   +N      O   2  CD3    CH3    C3
 O    C   2   
 C3   C
 CH3  C      H1     H2     H3
 CD3  C
 H1   CH3
 H2   CH3
 H3   CH3 
*
* Formyl amino terminus.
RESIDUE  FRM
 C   +N      O   2 
 O    C   2
*
* N terminus 
RESIDUE  NTE
 HT1 +N 
 HT2 +N
 HT3 +N
 DT1 +N
 DT2 +N
 DT3 +N 
*   
RESIDUE  NTR
 HT1 +N
 HT2 +N
 HT3 +N
 DT1 +N
 DT2 +N
 DT3 +N 
* 
RESIDUE  NME
 N    CT     HN
 CT   N      HT1    HT2    HT3
 HN   N
 HT1  CT
 HT2  CT
 HT3  CT
* C terminus 
RESIDUE  CTE
 OT2 -C
*
RESIDUE  CTR
 OT2 -C
*
RESIDUE  CTE
 OXT -C
* Methylated amino terminus
RESIDUE  CBX
 CH3 +N
 C3  +N
* 
END
