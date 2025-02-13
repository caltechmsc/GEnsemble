#!/usr/bin/env perl

use warnings;

use Getopt::Long;
use LWP::Simple;

if (@ARGV == 0) { help(); }

GetOptions ('h|help'        => \$help,
            's|ssp=s'       => \$ssp,
            'm|mfta=s'      => \$mfta_in,
            'o|out=s'       => \$out,
            );

if ($help) { help(); }
if (!$ssp) {die "Must specify the .ssp file!\nFor Help: update_mfta.pl -h\n\n"; }
if (!$mfta_in) {die "Must specify the .mfta file to update!\nFor Help: update_mfta.pl -h\n\n"; }
if (!$out) {($out = $mfta_in) =~ s/.mfta/.ssp.mfta/; }

open(SSP_FILE, $ssp);
while (<SSP_FILE>){
                  while ( /^NEW_RAW/g ){push @new_raw, $_;}
                  while ( /^NEW_CAP/g ){push @new_cap, $_;}
                  }
close SSP_FILE;

$join_raw = join ("", @new_raw);
$join_raw =~ s/NEW_RAW:   //g;
$join_raw =~ s/\n//g;
@split_raw = split ("",$join_raw);

$join_cap = join ("", @new_cap);
$join_cap =~ s/NEW_CAP:   //g;
$join_cap =~ s/\n//g;
#print $join_cap;
@split_cap = split ("",$join_cap);
#print "@split_cap";
# search for ?, if found kill #
#foreach (@split_cap) {
if ($join_cap =~ m/\?/) {die "Error: found ? in the ssp file. \nssp file needs to be manually edited!!\n\n"; }
#                     }

my (@array_raw) = @split_raw;
my $search_H = "H";
my $search_C = "-";
for ($i = 0; $i < 7; $i++){
                           my ($index) = grep $array_raw[$_] eq $search_H, 0 .. $#array_raw;
                           scalar($index); 
                           push @raw, $index;
                           for ($j = 0; $j < $index; $j++){shift @array_raw;}
                           
                           my ($index2) = grep $array_raw[$_] eq $search_C, 0 .. $#array_raw;
                           scalar($index2);
                           push @raw, $index2-1;
                           for ($j = 0; $j < $index2; $j++){shift @array_raw;}
                          }
my @added_raw;
$added_raw[0] = $raw[0]+1;
$added_raw[1] = $raw[1]+$added_raw[0];
$added_raw[2] = $raw[2]+$added_raw[1]+1;
$added_raw[3] = $raw[3]+$added_raw[2];
$added_raw[4] = $raw[4]+$added_raw[3]+1;
$added_raw[5] = $raw[5]+$added_raw[4];
$added_raw[6] = $raw[6]+$added_raw[5]+1;
$added_raw[7] = $raw[7]+$added_raw[6];
$added_raw[8] = $raw[8]+$added_raw[7]+1;
$added_raw[9] = $raw[9]+$added_raw[8];
$added_raw[10] = $raw[10]+$added_raw[9]+1;
$added_raw[11] = $raw[11]+$added_raw[10];
$added_raw[12] = $raw[12]+$added_raw[11]+1;
$added_raw[13] = $raw[13]+$added_raw[12];

my (@array_cap) = @split_cap;
for ($i = 0; $i < 7; $i++){
                           my ($index3) = grep $array_cap[$_] eq $search_H, 0 .. $#array_cap;
                           scalar($index3);
                           push @cap, $index3;
                           for ($j = 0; $j < $index3; $j++){shift @array_cap;}

                           my ($index4) = grep $array_cap[$_] eq $search_C, 0 .. $#array_cap;
                           scalar($index3);
                           push @cap, $index4-1;
                           for ($j = 0; $j < $index4; $j++){shift @array_cap;}
                           }
my @added_cap;
$added_cap[0] = $cap[0]+1;
$added_cap[1] = $cap[1]+$added_cap[0];
$added_cap[2] = $cap[2]+$added_cap[1]+1;
$added_cap[3] = $cap[3]+$added_cap[2];
$added_cap[4] = $cap[4]+$added_cap[3]+1;
$added_cap[5] = $cap[5]+$added_cap[4];
$added_cap[6] = $cap[6]+$added_cap[5]+1;
$added_cap[7] = $cap[7]+$added_cap[6];
$added_cap[8] = $cap[8]+$added_cap[7]+1;
$added_cap[9] = $cap[9]+$added_cap[8];
$added_cap[10] = $cap[10]+$added_cap[9]+1;
$added_cap[11] = $cap[11]+$added_cap[10];
$added_cap[12] = $cap[12]+$added_cap[11]+1;
$added_cap[13] = $cap[13]+$added_cap[12];
                          
open(MFTA_FILE, $mfta_in);
while (<MFTA_FILE>){
                   while ( /^\*  \d+tm/g ){push @tml, $_;}
                   while ( /^\*  \d+hp/g ){push @hp, $_;}
                   s/\*.*//;
                   next if /^(\s)*$/;
                   chomp;
                   push @mfta, $_;
                   }
close MFTA_FILE;
$length_mfta = scalar(@mfta);

for ($i=0; $i < 7; $i++) {
    @tmp = split(/\s+/,$tml[$i]);
    for ($j=0 ; $j<$#tmp+1 ; $j++) {
        $tm[$i][$j]=$tmp[$j];
    }
    $tm[$i][6] = $added_raw[$i*2];
    $tm[$i][7] = $added_raw[$i*2+1];
    $tm[$i][8] = $added_cap[$i*2];
    $tm[$i][9] = $added_cap[$i*2+1];
}

open(MFTA_OUT, ">$out");
for ($i = 0; $i < $length_mfta; $i++){print MFTA_OUT $mfta[$i] . "\n";}

for ($i=0; $i < 7; $i++) {
printf MFTA_OUT "*  %3s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s\n", $tm[$i][1], $tm[$i][2], $tm[$i][3], $tm[$i][4], $tm[$i][5], $tm[$i][6], $tm[$i][7], $tm[$i][8], $tm[$i][9], $tm[$i][10], $tm[$i][11], $tm[$i][12];
}
for ($i = 0; $i < 7; $i++){print MFTA_OUT $hp[$i];}
close(MFTA_OUT);
exit;

sub help {
         my $help = 
"
Program:
 :: update_mfta.pl

Author:
 :: Bartosz Trzaskowski (trzask\@wag.caltech.edu)

Usage:
 :: update_mfta.pl -s {secondary structure prediction} -m {input mfta file} -o {output mfta file; optional}

Description:
 :: This script takes a secondary structure prediction
 :: from format_secondary.pl script and based on the
 :: NEW_RAW and NEW_CAP lines updates the mfta file.
 ::
 :: For a complete description check:
 :: https://wiki.wag.caltech.edu/twiki/bin/view/Biogroup/Secondary_Page
";         
         die "$help";
         }
       
