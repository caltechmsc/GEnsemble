#!/bin/csh

#r/\\/i, 04/09/2007 version.1
# added all scream and penalty
#
# This batch file will run several rotations and minimizations
# on a series of rotations to get all combinations
# written by: Spencer Hall 2/05/2004
#
# rotmin {name} {Prefix} {1 = lipid, 0 = no lipid}
#        {Unix machine name} {linux number} {SGI temp}
#
# The input files are:
#      min_CDrotmin.ctl - The template minimization .ctl filea
#      min_CD_m2.ctl    - 1st full minimization no fixed atoms
#      {Prefix}.CD.rot  - 1st 7 lines contain the rotations to be run
#                         (35 45 ...) per line, line # = Helix #
#
# The output files are:
#      {Prefix}.?-?-?-?-?-?-?.bgf - Output of degrees and rotations
#      {Prefix}.CDrotmin.out      - Total Energy output
#      {prefix}.CDrotmin.ED       - Energy Decomposition output
#
# Needed files are:
#      nacl-append       - Access to adding counter-ions
#      HsprotL.exe       - Rotation code in Fortran
#
# The bundle should be minimized before this script runs.
# Do not have counterions in your bundle, this script will do it!
# Your file will run smoother if it is version 332.

# Minimize the starting file to make it run faster
# Create the template min.ctl file

# Create a smaller named file

set template = ${1}
set protein  = ${2}
set angles   = ${3}
set mydir    = ${4}
hostname

cp ${template} ${protein}.bgf

# Get the number of atoms in helix 1 through helix 7
# Also get the degrees to search for each helix
set nh1=`awk 'BEGIN {n=0;h=0;s=0};$1=="ATOM" {$5=substr($0,26,5)+0;if (s==1) {if (n!=$5) {n=n+1;if (n!=$5) {h=h+1;if (h==1){print "1 "$2-1};s=0}}} else {s=1;n=$5}}' ${protein}.bgf`

awk '{if (FNR == 1) {print $0}}' $angles > hel1.deg

set nh2=`awk 'BEGIN {n=0;h=0;s=0};$1=="ATOM" {$5=substr($0,26,5)+0;if (s==1) {if (n!=$5) {n=n+1;if (n!=$5) {h=h+1;if (h==1){b=$2};if (h==2){print b" "$2-1};s=0}}} else {s=1;n=$5}}' ${protein}.bgf`

awk '{if (FNR == 2) {print $0}}' $angles > hel2.deg

set nh3=`awk 'BEGIN {n=0;h=0;s=0};$1=="ATOM" {$5=substr($0,26,5)+0;if (s==1) {if (n!=$5) {n=n+1;if (n!=$5) {h=h+1;if (h==2){b=$2};if (h==3){print b" "$2-1};s=0}}} else {s=1;n=$5}}' ${protein}.bgf`

awk '{if (FNR == 3) {print $0}}' $angles > hel3.deg

set nh4=`awk 'BEGIN {n=0;h=0;s=0};$1=="ATOM" {$5=substr($0,26,5)+0;if (s==1) {if (n!=$5) {n=n+1;if (n!=$5) {h=h+1;if (h==3){b=$2};if (h==4){print b" "$2-1};s=0}}} else {s=1;n=$5}}' ${protein}.bgf`

awk '{if (FNR == 4) {print $0}}' $angles > hel4.deg

set nh5=`awk 'BEGIN {n=0;h=0;s=0};$1=="ATOM" {$5=substr($0,26,5)+0;if (s==1) {if (n!=$5) {n=n+1;if (n!=$5) {h=h+1;if (h==4){b=$2};if (h==5){print b" "$2-1};s=0}}} else {s=1;n=$5}}' ${protein}.bgf`

awk '{if (FNR == 5) {print $0}}' $angles > hel5.deg

set nh6=`awk 'BEGIN {n=0;h=0;s=0};$1=="ATOM" {$5=substr($0,26,5)+0;if (s==1) {if (n!=$5) {n=n+1;if (n!=$5) {h=h+1;if (h==5){b=$2};if (h==6){print b" "$2-1};s=0}}} else {s=1;n=$5}}' ${protein}.bgf`

awk '{if (FNR == 6) {print $0}}' $angles > hel6.deg

set nh7=`awk 'BEGIN {n=0;h=0;s=0};$1=="ATOM" {c=$2;$5=substr($0,26,5)+0;if (s==1) {if (n!=$5) {n=n+1;if (n!=$5) {h=h+1;if (h==6){b=$2};s=0}}} else {s=1;n=$5}};END {print b" "c}' ${protein}.bgf`

awk '{if (FNR == 7) {print $0}}' $angles > hel7.deg

set name = ${protein}

echo "Starting combinatorial rotations now..."

# This will start loops for each of the 7 helices
foreach hel1 (`cat hel1.deg`)
foreach hel2 (`cat hel2.deg`)
foreach hel3 (`cat hel3.deg`)
foreach hel4 (`cat hel4.deg`)
foreach hel5 (`cat hel5.deg`)
foreach hel6 (`cat hel6.deg`)
foreach hel7 (`cat hel7.deg`)
echo "done with starting the loops"

set deg = ${hel1}_${hel2}_${hel3}_${hel4}_${hel5}_${hel6}_${hel7}
echo "degrees =" $deg " "

# Make input file for rotations
cat > ini.02052004 << EOF
${name}.bgf
${name}.${deg}.combirot.bgf
${nh1} 0
0.0
0
${hel1}
${nh2} 1
0.0
0
${hel2}
${nh3} 0
0.0
0
${hel3}
${nh4} 1
0.0
0
${hel4}
${nh5} 0
0.0
0
${hel5}
${nh6} 1
0.0
0
${hel6}
${nh7} 0
0.0
0
${hel7}
0 0 0
EOF

# Run rotational code
$mydir/annex/HsprotL.exe < ini.02052004

echo "done with rotations"
 
end
end
end
end
end
end
end

# Clean-up files
#cp *.bgf ${startdir}
#cd ${startdir}
#/bin/rm -fr ${tmpdr}/$USER/${unique}
