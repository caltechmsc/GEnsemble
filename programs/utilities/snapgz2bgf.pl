#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use Cwd;
use File::Copy;
use File::Path;
use Getopt::Long;
use POSIX qw(ceil);
use Sys::Hostname;
use Time::Local;

# Get Input Information
GetOptions ('h|help'                => \$help,
	    's|snaps=s'             => \$snapinput,
	    't|template=s'          => \$template,
	    'skip=i'                => \$skip,);

if (!$snapinput || !$template) { &help(); }
if ($help) { &help(); }

@snaps = glob "$snapinput";

@sortsnaps = sort sort_snapshots (@snaps);

foreach $snap (@sortsnaps) {
    $snap =~ /(\S+).snap(\d+)/;
    if ($2 >= $skip) {
	if ($snap =~ /.gz$/) {
	    ($snap_prefix = $snap) =~ s/.gz$//;
	    ($snap_bgf    = $snap) =~ s/.gz$/.bgf/;
	    `gunzip $snap`;
	    `${Bin}/snap2bgfL $snap_prefix $template > $snap_bgf`;
	    `gzip $snap_prefix`;
	} else {
	    $snap_bgf = $snap . ".bgf";
	    `${Bin}/snap2bgfL $snap $template > $snap_bgf`;
	}
    }
}

sub sort_snapshots {

    $a =~ /snap(\d+)/;
    $a1 = $1;

    $b =~ /snap(\d+)/;
    $b1 = $1;

    if ($a1 < $b1) { return -1; }
    if ($a1 > $b1) { return 1; }
    if ($a1 == $b1) { return 0; }
    return 0;
}

sub help {
    $help_message = "
Program:
 :: snapgz2bgf.pl

Author:
 :: Adam R. Griffith (griffith\@wag.caltech.edu)

Usage:
 :: snapgz2bgf.pl -s {snap file with wildcards}

Options:
 :: -h | --help             :: Optional :: No Input
 :: Prints this help message.

 :: -s | --snaps            :: Required :: Filename Template
 :: The filename template (with wildcards) of the snapshot
 :: or gzipped snapshots (with .gz file extension) to be
 :: converted to BGF.  Note that quotes are required when
 :: wildcards are being used.
 :: Ex: -s 'd5-helix1-neimo.snap*.gz'

 :: -t | --template         :: Required :: Filename
 :: The BGF template file that corresponds to the snap file.

 :: -n | --neutralize       :: Optional :: No Input
 :: Using this flag will cause the template to be neutralized
 :: using /ul/victor/utilities/Neutral-Prep/Neutral-Prep.pl
 :: before the snap->BGF conversions.

Description:
 :: This program converts snapshot files to BGF files.  If the
 :: snapshots are gzipped and have a .gz file extension, then
 :: the snapshot will be unzipped, converted to BGF, and then
 :: the snapshot will be gzipped again.

";
    die $help_message;
}
