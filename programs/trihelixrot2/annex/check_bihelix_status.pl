#!/usr/bin/perl

my $wait = 1;
while ($wait) {
	$wait = 0;
	$ncount = qx(ls */*bihelix_done* | wc -l);
	if ($ncount != 12) {
	$wait = 1;
	sleep 60;
	}
}
