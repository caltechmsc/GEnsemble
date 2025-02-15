#!/usr/bin/perl

$infile = @ARGV[0];
$outfile = @ARGV[1];

if (substr($infile, -4, 4) ne '.bgf') {
    print "Running this program on a file that isn\'t a bgf will have horrible consequences... \nI really don\'t think you want to do this.\n";
    exit;
}

open(IN, $infile);
@FILE=<IN>;
close(IN);


open(OUT, ">$outfile");

while($line = shift(@FILE)) {
    if ((substr($line, 0, 4) eq "ATOM")) {
	substr($line, 23, 1) = "A";
    }
    if ($line =~ /HETATM/) {
	substr($line, 23, 1) = "B";
    }
    print OUT $line;
}

 
