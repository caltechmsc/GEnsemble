#!/usr/bin/perl

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

use Cwd;
use File::Copy;
use Getopt::Long;
use POSIX qw(ceil floor);
use Sys::Hostname;
use Time::Local;

@bgfs = @ARGV;

foreach $bgf (@bgfs) {
    open BGF, "$bgf";
    @LINES = <BGF>;
    close BGF;

    open BGF, ">$bgf";
    foreach $line (@LINES) {
	if ($line =~ /^FORMAT ATOM/) {
	    print BGF "FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x,a1,1x,a5,3f10.5,1x,a5,i3,i2,1x,f8.5,i2,i4,f10.5)\n";
	} else {
	    print BGF "$line";
	}
    }
    close BGF;
}

exit;
