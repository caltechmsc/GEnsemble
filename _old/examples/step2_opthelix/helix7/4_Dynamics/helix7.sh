#!/bin/csh
setenv MPSIM_DATA /home/ravi/GEnsemble/programs/mpsim/mpsimdata
/home/ravi/GEnsemble/programs/mpsim/mpsim helix7.3.50_K.ctl > helix7.3.50_K.out
/home/ravi/GEnsemble/programs/mpsim/mpsim helix7.3.100_K.ctl > helix7.3.100_K.out
/home/ravi/GEnsemble/programs/mpsim/mpsim helix7.3.150_K.ctl > helix7.3.150_K.out
/home/ravi/GEnsemble/programs/mpsim/mpsim helix7.3.200_K.ctl > helix7.3.200_K.out
/home/ravi/GEnsemble/programs/mpsim/mpsim helix7.3.250_K.ctl > helix7.3.250_K.out

cp helix7.3.250_K.fin.bgf helix7.4.pre_dynamics.bgf

/home/ravi/GEnsemble/programs/mpsim/mpsim -s5000 helix7.5.dynamics.ctl  > helix7.5.dynamics.out
/home/ravi/GEnsemble/programs/utilities/snapgz2bgf.pl -s 'helix7.5.dynamics.snap*' -t helix7.4.pre_dynamics.bgf --skip 254999 >& helix7.5.dynamics.eng
/home/ravi/GEnsemble/programs/utilities/bgf_snap_rmsd -m -v -t helix7.4.pre_dynamics.bgf helix7.5.dynamics.snap254999 5000 150 > helix7.5.dynamics.rmsd
/home/ravi/GEnsemble/programs/utilities/bgf_match.pl -p helix7.5.dynamics.snap -f 254999 -i 5000 -n 150

mkdir helix7.3.warmup
mv helix7.3.*.* helix7.3.warmup
gzip -r helix7.3.warmup

mkdir helix7.5.dynamics.bgfs
/home/ravi/GEnsemble/programs/utilities/multi_bgf2pdb.pl helix7.5.dynamics.snap*.bgf
mv *.bgf helix7.5.dynamics.bgfs

mkdir helix7.5.dynamics.pdbs
mv *.pdb helix7.5.dynamics.pdbs
gzip -r helix7.5.dynamics.pdbs

mkdir helix7.5.dynamics.snaps
mv *.snap* helix7.5.dynamics.snaps
gzip -r helix7.5.dynamics.snaps

gzip helix7.5.dynamics.ctl
gzip helix7.5.dynamics.traj1
gzip helix7.5.dynamics.rst
gzip helix7.5.dynamics.out
touch _dyn_finished_

