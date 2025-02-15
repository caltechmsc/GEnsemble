#!/usr/bin/perl -w

BEGIN {
    use FindBin qw($Bin);
    use lib $FindBin::Bin;
}

foreach $bgf (@ARGV) {
    if ($bgf =~ /.bgf$/) {
	($pdb = $bgf) =~ s/.bgf$/.pdb/;
	`${Bin}/bgf2pdb.pl $bgf > $pdb`;
    }
}
