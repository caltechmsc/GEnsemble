#######################################
#  DO NOT CHANGE THIS FOR ANY REASON  #
#######################################
#
#  MSI Shell Script Setup file      	(c) 1992 Molecular Simulations, Inc.
#
setenv BIOVER	330
setenv memtmp1 /temp1
set remakedir=${memtmp1}/biogv${BIOVER}/remakes/$USER
setenv MSIUSR	${membstruk}/Biograf
setenv BG_BASE	$MSIUSR/biogv$BIOVER
setenv BG_EXE	$BG_BASE/exe
# setenv BIOHOST `${membstruk}/Biograf/biodesign.a` # Failes on read FF
setenv BIOHOST iris

#
if ($?LOGNAME == 0) then
	if ($?USER != 0) then
		setenv LOGNAME	$USER
	else
		setenv LOGNAME	`whoami`
	endif
endif
#
if ($?BG_SCR == 0)	setenv BG_SCR	${memtmp1}/${LOGNAME}_
#
if ((! -d /usr/dore/data/fonts) && $?DORE_FONTDATA == 0) then
	setenv DORE_FONTDATA	$BG_BASE/dore/dorefonts
        setenv DORE_FONTDIR    $BG_BASE/dore/dorefonts
endif
if ((! -f /usr/dore/data/errmsg/errmsgfile) && $?DORE_ERRDATA == 0) then
	setenv DORE_ERRDATA	$BG_BASE/dore/errmsg
        setenv DORE_ERRMSGFILE     $BG_BASE/dore/errmsg/errmsgfile
endif
#
setenv FOR099	$BG_EXE/auth${BIOVER}.fil
#
alias comstruct	"$BG_EXE/comst${BIOVER}_$BIOHOST"
alias getsn	$BG_EXE/getsn_$BIOHOST
alias rdtrj	$BG_EXE/rdtrj${BIOVER}_$BIOHOST
alias wrtrj	$BG_EXE/wrtrj${BIOVER}_$BIOHOST
alias shtrj	$BG_EXE/shtrj${BIOVER}_$BIOHOST
#
setenv BG_CARBO		$BG_BASE/carbohydrate/
setenv BG_DATA		$BG_BASE/data/
setenv BG_DNA_DOUBLE	$BG_BASE/dna/double/
setenv BG_DNA_SINGLE	$BG_BASE/dna/single/
setenv BG_DNA_TRIPLE	$BG_BASE/dna/triple/
setenv BG_LIPID_BCK	$BG_BASE/lipid/backbone/
setenv BG_LIPID_FA	$BG_BASE/lipid/fatty_acid/
setenv BG_LIPID_HG	$BG_BASE/lipid/head_group/
setenv BG_MACRO		$BG_BASE/macro/
setenv BG_MONOMER	$BG_BASE/monomer/
setenv BG_ORG_FRG	$BG_BASE/organic/fragment/
setenv BG_ORG_FUN	$BG_BASE/organic/function/
setenv BG_PEP		$BG_BASE/peptide/
setenv BG_PEP_D		$BG_BASE/peptide_d/
setenv BG_PEP_L		$BG_BASE/peptide_l/
setenv BG_POLARIS	$BG_BASE/polaris/
setenv BG_SIDE		$BG_BASE/sidechains/
setenv BG_SOLVENT	$BG_BASE/solvent/
#
#  lowercase versions of environment variables
#
setenv bg_carbo		$BG_CARBO
setenv bg_data		$BG_DATA
setenv bg_dna_double	$BG_DNA_DOUBLE
setenv bg_dna_single	$BG_DNA_SINGLE
setenv bg_dna_triple	$BG_DNA_TRIPLE
setenv bg_exe		$BG_EXE
setenv bg_lipid_bck	$BG_LIPID_BCK
setenv bg_lipid_fa	$BG_LIPID_FA
setenv bg_lipid_hg	$BG_LIPID_HG
setenv bg_macro		$BG_MACRO
setenv bg_monomer	$BG_MONOMER
setenv bg_org_frg	$BG_ORG_FRG
setenv bg_org_fun	$BG_ORG_FUN
setenv bg_pep		$BG_PEP
setenv bg_pep_d		$BG_PEP_D
setenv bg_pep_l		$BG_PEP_L
setenv bg_polaris	$BG_POLARIS
setenv bg_scr		$BG_SCR
setenv bg_side		$BG_SIDE
setenv bg_solvent	$BG_SOLVENT
#
