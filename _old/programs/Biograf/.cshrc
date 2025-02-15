#!/bin/csh

setenv membstruk /home/ravi/GEnsemble/programs
alias bgver 'setenv BIOVER \!:*; source ${membstruk}/Biograf/bg_login.csh'
	alias xtlver bgver

	if ( $?BIOVER == 0 ) then
		bgver 330
	endif

	set hosttype = `${membstruk}/Biograf/biodesign.a`

	if ($hosttype == fx) then
	 set default = 390
	else
	 set default = $hosttype
	endif

#
# Alias set up for the Linux version
#
        alias bioamb  "${membstruk}/Biograf/bio_linux $default amber"
        alias biobio  "${membstruk}/Biograf/bio_linux $default Biograf"
        alias biodre  "${membstruk}/Biograf/bio_linux $default dreidi"
        alias biodr2  "${membstruk}/Biograf/bio_linux $default dreidii"
	alias biogen  "${membstruk}/Biograf/bio_linux $default genff"
	alias biomm2  "${membstruk}/Biograf/bio_linux $default mm2"
	alias biomp2  "${membstruk}/Biograf/bio_linux $default mmp2"
        alias biouff  "${membstruk}/Biograf/bio_linux $default uff"

