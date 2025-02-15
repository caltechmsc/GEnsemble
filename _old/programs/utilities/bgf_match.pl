#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use Cwd;
use File::Copy;
use Getopt::Long;
use POSIX qw(ceil);
use Sys::Hostname;
use Time::Local;

##### MAIN ROUTINE #####
# Get Input Information
GetOptions ('h|help'           => \$help,
	    'p|prefix=s'       => \$prefix,
	    'f|firstsnap=i'    => \$firstsnap,
	    'i|snapinterval=i' => \$snapinterval,
	    'n|numsnaps=i'     => \$numsnaps);

if ($help) { help(); }
if ((!$prefix) || (!$firstsnap) || (!$snapinterval) || (!$numsnaps)) { help(); }

$template = "${prefix}${firstsnap}.bgf";
for ($i = 1; $i < $numsnaps; $i++) {
    $snap     = $firstsnap + ($i * $snapinterval);
    $filename = "${prefix}${snap}.bgf";

    `${Bin}/bgf_match $template $filename > tmp.bgf`;
    move("tmp.bgf","$filename");
}

exit;

sub help {
    $help_message = "
Program:
 :: bgf_match.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: bgf_match.pl -p {prefix} -f {firstsnapshot}
 ::              -i {snap interval} -n {number of snaps}

Options:
 :: -h | --help             :: Optional :: No Input
 :: Prints this help message.

 :: -p | --prefix           :: Required :: String
 :: This is the prefix (without snapshot number) of the
 :: first snapshot in the trajectory.  For example,
 :: if the first snapshot BGF is:
 ::    helix1.4.dyn.snap999.bgf
 :: then the proper input for -p is:
 ::    -p helix1.4.dyn.snap

 :: -f | --firstsnap        :: Required :: Integer
 :: This is the step number of the first snapshot in
 :: the trajectory.  For example, if the first snapshot
 :: BGF is:
 ::    helix1.4.dyn.snap999.bgf
 :: then the proper input for -f is:
 ::    -f 999

 :: -i | --snapinterval     :: Required :: Integer
 :: This is the number of steps between snapshots in
 :: the trajectory.  For example, if the first 2 snapshots
 :: are:
 ::    helix1.4.dyn.snap999.bgf, helix1.4.dyn.snap1999.bgf
 :: then the proper input for -i is:
 ::    -i 1000

 :: -n | --numsnaps         :: Required :: Integer
 :: This is the total number of snapshots in the trajectory,
 :: including the first one.  For example, if the snapshots
 :: range from snap999 to snap499999, then the proper input
 :: for -n is 500.

Description:
 :: This program aligns snapshot BGF files from a dynamics
 :: trajectory to the first snapshot BGF using bgf_match,
 :: which must be in the same directory as bgf_match.pl
 ::
 :: Note that all of the snapshot BGF files will be overwritten
 :: with their realigned structures, so make sure to back up
 :: your files elsewhere if you wish to keep the originals.

";
    die $help_message;
}
