#!/bin/csh
# This is a installer file for setting up Biograf Linux on the system
# This should only be run on systems that have MembStruk installed

# This is to setup the FF file links for MembStruk
cd biogv330/exe/

rm -f Biograf330.par
rm -f Biograf-qeq330.par
rm -f Biograf330.cnv
rm -f Biograf-qeq330.cnv
ln -s /project/Biogroup/membstruk2/FF/Biograf.par Biograf330.par
ln -s /project/Biogroup/membstruk2/FF/Biograf.par Biograf-qeq330.par
ln -s /project/Biogroup/membstruk2/FF/Biograf.cnv Biograf330.cnv
ln -s /project/Biogroup/membstruk2/FF/Biograf-qeq.cnv Biograf-qeq330.cnv


