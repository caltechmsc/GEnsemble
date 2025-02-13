#!/usr/bin/env perl

#use warnings;

use Getopt::Long;
use LWP::Simple;

if (@ARGV == 0) { help(); }

GetOptions ('h|help'        => \$help,
            'e|expasy=s'    => \$expasy,
            'm|mfta=s'      => \$mfta_in,
            'a|apssp2=s'    => \$apssp2_in,
            'p|porter=s'    => \$porter_in,
            'd|psipred=s'   => \$psipred_in,
            's|sspro=s'     => \$sspro_in,
            'j|jpred=s'     => \$jpred_in,
            'o|out=s'       => \$output,
            );

if ($help) { help(); }
if (!$mfta_in && !$expasy) {die "Must specify either MFTA or EXPASY!\nFor Help: format_secondary.pl -h\n\n"; }
if (!$apssp2_in && !$porter_in && !$psipred_in && !$sspro_in) { die "Must specify at least one of APSSP2, PORTER, PSIPRED or SSPRO!\nFor Help: format_secondary.pl -h\n\n"; }
if (!$output) {
              if (defined $mfta_in) {($output = $mfta_in) =~ s/.mfta/.ssp/; }
           elsif (defined $expasy) {$output = "$expasy.ssp"; }
              }

if (defined $expasy){
                    my $url =
                    "http://www.uniprot.org/uniprot/"  .
                    "$expasy"  .
                    ".fasta"   ;
                   $html = get $url;
                   die "Blast :: Could not load BLAST HTML results.\n" unless defined $html;
                   open FASTA, ">$expasy.fasta"; print FASTA "$html"; close FASTA;
                   }

if (defined $mfta_in) {
                    open(MFTA_FILE, $mfta_in);
                    while( <MFTA_FILE> ) {
                        s/>.*//;
                        s/\*.*//;
                        next if /^(\s)*$/;
                        chomp;
                        push @mfta, $_;
                        }
                      }
elsif (defined $expasy){
                    open(MFTA_FILE, "$expasy.fasta");
                    while( <MFTA_FILE> ) {
                        s/>.*//;
                        next if /^(\s)*$/;
                        chomp;
                        push @mfta, $_;
                        }
                       }
                    close MFTA_FILE;
                    $length_mfta = scalar(@mfta);
                    $length_mfta_last = length($mfta[$length_mfta-1]);

if (defined $mfta_in) {
                    open(MFTA_FILE2, $mfta_in);
                    while( <MFTA_FILE2> ) {
                       s/>.*//;
                       s/^([A-Z]).*//;
                       next if /^(\s)*$/;
                       chomp;
                       push @mfta_pre, $_;
                       }
                      
                   close MFTA_FILE2;

                   for ( $i = 0; $i < 7; $i++) {
                                         @mfta_split = split( " ", $mfta_pre[$i]);
                                         push @mfta_raw_start, $mfta_split[2];
                                         push @mfta_raw_end, $mfta_split[3];
                                         push @mfta_cap_start, $mfta_split[4];
                                         push @mfta_cap_end, $mfta_split[5];
                                         }

                 push @mfta_raw, "-" x ($mfta_raw_start[0]-1);
                 for ( $i = 0; $i < 7; $i++) {
                            push @mfta_raw, "H" x (($mfta_raw_end[$i]-$mfta_raw_start[$i])+1);
                            push @mfta_raw, "-" x (($mfta_raw_start[$i+1]-$mfta_raw_end[$i]-1));
                                             }
                 push @mfta_raw, "-" x (((($length_mfta-1)*60)+$length_mfta_last)-$mfta_raw_end[6]);

                 push @mfta_cap, "-" x ($mfta_cap_start[0]-1);
                 for ( $i = 0; $i < 7; $i++) {
                            push @mfta_cap, "H" x (($mfta_cap_end[$i]-$mfta_cap_start[$i])+1);
                            push @mfta_cap, "-" x (($mfta_cap_start[$i+1]-$mfta_cap_end[$i])-1);
                                             }
                 push @mfta_cap, "-" x (((($length_mfta-1)*60)+$length_mfta_last)-$mfta_cap_end[6]);

                 push @mfta_capq, "-" x ($mfta_raw_start[0]-2) . "?";
                 for ( $i = 0; $i < 6; $i++) {
                            push @mfta_capq, "H" x (($mfta_raw_end[$i]-$mfta_raw_start[$i])+1) . "?";
                            push @mfta_capq, "-" x (($mfta_raw_start[$i+1]-$mfta_raw_end[$i])-3) . "?";
                                             }
                 push @mfta_capq, "H" x (($mfta_raw_end[6]-$mfta_raw_start[6])+1) . "?";
                 push @mfta_capq, "-" x (($mfta_raw_start[7]-$mfta_raw_end[6])-3);
                 push @mfta_capq, "-" x (((($length_mfta-1)*60)+$length_mfta_last)-$mfta_raw_end[6]-1);

                 $mfta_raw_joined = join "", $mfta_raw[0], $mfta_raw[1], $mfta_raw[2], $mfta_raw[3], $mfta_raw[4], $mfta_raw[5], $mfta_raw[6], $mfta_raw[7], $mfta_raw[8], $mfta_raw[9], $mfta_raw[10], $mfta_raw[11], $mfta_raw[12], $mfta_raw[13], $mfta_raw[14], $mfta_raw[15];
                 $mfta_cap_joined = join "", $mfta_cap[0], $mfta_cap[1], $mfta_cap[2], $mfta_cap[3], $mfta_cap[4], $mfta_cap[5], $mfta_cap[6], $mfta_cap[7], $mfta_cap[8], $mfta_cap[9], $mfta_cap[10], $mfta_cap[11], $mfta_cap[12], $mfta_cap[13], $mfta_cap[14], $mfta_cap[15];
                 $mfta_capq_joined = join "", $mfta_capq[0], $mfta_capq[1], $mfta_capq[2], $mfta_capq[3], $mfta_capq[4], $mfta_capq[5], $mfta_capq[6], $mfta_capq[7], $mfta_capq[8], $mfta_capq[9], $mfta_capq[10], $mfta_capq[11], $mfta_capq[12], $mfta_capq[13], $mfta_capq[14], $mfta_capq[15];
                 @mfta_raw_split = split( "", $mfta_raw_joined);
                 @mfta_cap_split = split( "", $mfta_cap_joined);
                 @mfta_capq_split = split( "", $mfta_capq_joined);
                 }

if (defined $apssp2_in){
            open(APSSP2_FILE, $apssp2_in); 
            while( <APSSP2_FILE> ) {
                        s/REMARK.*//;
                        s/METHOD.*//;
                        s/PFRMAT.*//;
                        s/TARGET.*//;
                        s/AUTHOR.*//;
                        s/MODEL.*//;
                        s/END.*//;
                        s/0\.//;
                        s/1\.//;
                        s/0/\*/;
                        s/C/c/g;
                        next if /^(\s)*$/;
                        chomp;
                        push @apssp2, $_;
                       }
            close APSSP2_FILE;
            $length_apssp2 = scalar(@apssp2);
            for ( $i = 0; $i < $length_apssp2; $i++) {
                                         @new_apssp2 = split( " ", $apssp2[$i]);                   
                                         push @ap1, $new_apssp2[0];
                                         push @ap2, $new_apssp2[1];
                                         push @ap3, $new_apssp2[2];
                                         }
            unshift (@ap1, "-");
            unshift (@ap1, "-");
            unshift (@ap2, "-");
            unshift (@ap2, "-");
            unshift (@ap3, "-");
            unshift (@ap3, "-");
            }

if (defined $porter_in){
            open(PORTER_FILE, $porter_in);
            while( <PORTER_FILE> ) {
                       s/C/c/g;
                       next if /^(\s)*$/;
                       chomp;
                       push @porter, $_;
                       }
            close PORTER_FILE;
            splice(@porter,0,4);
            }

if (defined $sspro_in){
            open(SSPRO_FILE, $sspro_in);
            while( <SSPRO_FILE> ) {
                       s/C/c/g;
                       next if /^(\s)*$/;
                       chomp;
                       push @sspro, $_;
                       }
            close SSPRO_FILE;
#            splice(@sspro,0,5);
            @sspro1 = split( "", $sspro[4]);
            }

if (defined $jpred_in){
            open(JPRED_FILE, $jpred_in);
            while( <JPRED_FILE> ) {
                       next if /^(\s)*$/;
                       next if /^Query/;
#                        tr/9/\*/;
#                        tr/8/9/;
#                        tr/7/8/;
#                        tr/6/7/;
#                        tr/5/6/;
#                        tr/4/5/;
#                        tr/3/4/;
#                        tr/2/3/;
#                        tr/1/2/;
#                        tr/0/1/;
                        tr/-/c/;
                       chomp;
                       push @jpred, $_;
                       }
            close JPRED_FILE;
            splice(@jpred,0,1);
            $length_jpred = scalar(@jpred);
            for ( $i = 0; $i < $length_jpred + 1; $i++) {
                                     @new_jpred = split (" ", $jpred[$i]);
                                     push @jpred1, $new_jpred[1];
                                                        }
#            print "@jpred";
            }


if (defined $psipred_in){
             open(PSIPRED_FILE, $psipred_in);
             while( <PSIPRED_FILE> ) {
                        s/PSIPRED.*//;
                        s/    .*//;
                        s/Key.*//;
                        s/#.*//;
                        s/Calculate.*//;
                        s/To.*//;
                        s/http.*//;
#                        tr/9/\*/;
#                        tr/8/9/;
#                        tr/7/8/;
#                        tr/6/7/;
#                        tr/5/6/;
#                        tr/4/5/;
#                        tr/3/4/;
#                        tr/2/3/;
#                        tr/1/2/;
#                        tr/0/1/;
                        s/C/c/g;
                        next if /^(\s)*$/;
                        chomp;
                        push @psipred, $_;
                       }
             close PSIPRED_FILE;
             $length_psipred = scalar(@psipred);
             for ( $i = 0; $i < $length_psipred + 1; $i++) {
                                         $psipred[$i] = substr($psipred[$i], 6);
                                         }
             }

open(OUTPUT_FILE, ">$output");

for ( $i = 0; $i < $length_mfta-1; $i++) {
                                      if ($i == 0)   {$spacer = 2; $aspacer = 1; $bspacer=1;}
                                      elsif ($i == 1){$spacer = 1; $aspacer = 1; $bspacer=0;}
                                      else           {$spacer = 0; $aspacer = 0; $bspacer=0;}
                                      $zspacer = 1;
                                      $s = $i * 60 + 1;
                                      $e = $i * 60 + 60;
                                      print OUTPUT_FILE " " x ($zspacer*18) . " " x $aspacer . ($s+9) . " " x ($zspacer*7) . " " x $aspacer . ($s+19) . " " x ($zspacer*7) . " " x $aspacer . ($s+29) ;
                                      print OUTPUT_FILE " " x ($zspacer*7) . " " x $bspacer . ($s+39) . " " x ($zspacer*7) . " " x $bspacer . ($s+49) . " " x ($zspacer*7) . " " x $bspacer . ($s+59) . "\n";
                                      print OUTPUT_FILE " " x ($zspacer*20) . "|" . " " x ($zspacer*9) . "|" . " " x ($zspacer*9) . "|" . " " x ($zspacer*9) . "|" . " " x ($zspacer*9) . "|" . " " x ($zspacer*9) . "|" . "\n";
                                      print OUTPUT_FILE "    SEQ:   " . "$mfta[$i]";
                                      if (defined $mfta_in)  {
                                                             print OUTPUT_FILE "\nNEW_RAW:   ";
                                                             for ( $j = $i * 60; $j < ($i * 60) + 60; $j++) {
                                                                                print OUTPUT_FILE "$mfta_raw_split[$j]";
                                                                                                            }
                                                             print OUTPUT_FILE "\nNEW_CAP:   ";
                                                             for ( $j = $i * 60; $j < ($i * 60) + 60; $j++) {
                                                                                print OUTPUT_FILE "$mfta_capq_split[$j]";
                                                                                                           } 
                                                             }
                                      if (defined $porter_in){
                                                             print OUTPUT_FILE "\n PORTER:   ";
                                                             print OUTPUT_FILE "$porter[2*$i+1]";
                                                             }
                                      if (defined $sspro_in){
                                                             print OUTPUT_FILE "\n  SSPRO:   ";
                                                             for ( $j = $i * 60; $j < ($i * 60) + 60; $j++) {
                                                                                                 print OUTPUT_FILE "$sspro1[$j]";
                                                                                                 }
                                                             }
                                      if (defined $apssp2_in){
                                                             print OUTPUT_FILE "\n APSSP2:   ";
                                                             for ( $j = $i * 60; $j < ($i * 60) + 60; $j++) {
                                                                                                 print OUTPUT_FILE "$ap2[$j]";
                                                                                                 }
                                                             print OUTPUT_FILE "\n APSSP2:   ";
                                                             for ( $j = $i * 60; $j < ($i * 60) + 60; $j++) {
                                                                                                 print OUTPUT_FILE "$ap3[$j]";
                                                                                                 }
                                                  }
                                      if (defined $psipred_in){
                                                              print OUTPUT_FILE "\nPSIPRED:   ";
                                                              print OUTPUT_FILE "$psipred[3*$i+1]";
                                                              print OUTPUT_FILE "\nPSIPRED:   ";
                                                              print OUTPUT_FILE "$psipred[3*$i+0]";
                                                              }
                                      if (defined $jpred_in){
                                                             print OUTPUT_FILE "\n  JPRED:   ";
                                                             print OUTPUT_FILE "$jpred1[2*$i+0]";
                                                             print OUTPUT_FILE "\n  JPRED:   ";
                                                             print OUTPUT_FILE "$jpred1[2*$i+1]";
                                                             }
                                      if (defined $mfta_in)   {
                                                              print OUTPUT_FILE "\nOLD_RAW:   ";
                                                              for ( $j = $i * 60; $j < ($i * 60) + 60; $j++) {
                                                                                 print OUTPUT_FILE "$mfta_raw_split[$j]";
                                                                                                             }
                                                              print OUTPUT_FILE "\nOLD_CAP:   ";
                                                              for ( $j = $i * 60; $j < ($i * 60) + 60; $j++) {
                                                                                 print OUTPUT_FILE "$mfta_cap_split[$j]";
                                                                                                            }
                                                             }
                                      print OUTPUT_FILE "\n";
                                      print OUTPUT_FILE "\n";
                                      }
$spacer = 0;
$zspacer = 1;
$aspacer = $bspacer = 0;
$k = $length_mfta-1;
$s = $k * 60 + 1;
$e = $k * 60 + $length_mfta_last;
print OUTPUT_FILE " " x ($zspacer*18) . ($s+9);
for ( $i = 1; $i < (($length_mfta_last/10)-1); $i++){
                                                 print OUTPUT_FILE " " x ($zspacer*7) . ($s+9+($i*10));
                                                 }
print OUTPUT_FILE "\n";
print OUTPUT_FILE " " x ($zspacer*20) . "|";
for ( $i = 1; $i < (($length_mfta_last/10)-1); $i++){
                                                 print OUTPUT_FILE " " x ($zspacer*9) . "|";
                                                 }
print OUTPUT_FILE "\n";
print OUTPUT_FILE "    SEQ:   " . "$mfta[$k]\n";
if (defined $mfta_in)  {
                       print OUTPUT_FILE "NEW_RAW:   ";
                       for ( $j = $k * 60; $j < ($k * 60) + 60; $j++) {
                                                            print OUTPUT_FILE "$mfta_raw_split[$j]";
                                                            }
                       print OUTPUT_FILE "\nNEW_CAP:   ";
                       for ( $j = $k * 60; $j < ($k * 60) + 60; $j++) {
                                                            print OUTPUT_FILE "$mfta_capq_split[$j]";
                                                            }
                       }  
if (defined $porter_in){
                       print OUTPUT_FILE "\n PORTER:   ";
                       print OUTPUT_FILE "$porter[2*$k+1]";
                       }
if (defined $sspro_in){
                       print OUTPUT_FILE "\n  SSPRO:   ";
                       for ( $j = $k * 60; $j < ($k * 60) + 60; $j++) {
                                                            print OUTPUT_FILE "$sspro1[$j]";
                                                           }
                       }
if (defined $apssp2_in){
                       print OUTPUT_FILE "\n APSSP2:   ";
                       for ( $j = $k * 60; $j < ($k * 60) + 60; $j++) {
                                                            print OUTPUT_FILE "$ap2[$j]";
                                                           }
                       print OUTPUT_FILE "\n APSSP2:   ";
                       for ( $j = $k * 60; $j < ($k * 60) + 60; $j++) {
                                                            print OUTPUT_FILE "$ap3[$j]";
                                                           }
                       }
if (defined $psipred_in){
                        print OUTPUT_FILE "\nPSIPRED:   ";
                        print OUTPUT_FILE "$psipred[3*$k+1]";
                        print OUTPUT_FILE "\nPSIPRED:   ";
                        print OUTPUT_FILE "$psipred[3*$k+0]";
                        }
if (defined $jpred_in){
                       print OUTPUT_FILE "\n  JPRED:   ";
                       print OUTPUT_FILE "$jpred1[2*$k+0]";
                       print OUTPUT_FILE "\n  JPRED:   ";
                       print OUTPUT_FILE "$jpred1[2*$k+1]";
                       }
if (defined $mfta_in)   {
                        print OUTPUT_FILE "\nOLD_RAW:   ";
                        for ( $j = $k * 60; $j < ($k * 60) + 60; $j++) {
                                                             print OUTPUT_FILE "$mfta_raw_split[$j]";
                                                             }
                        print OUTPUT_FILE "\nOLD_CAP:   ";
                        for ( $j = $k * 60; $j < ($k * 60) + 60; $j++) {
                                                             print OUTPUT_FILE "$mfta_cap_split[$j]";
                                                             }
                        print OUTPUT_FILE "\n";
                        }
print OUTPUT_FILE " \n";


print OUTPUT_FILE " 
KEY:

SEQ: sequence
NEW_RAW: raw prediction from PredicTM to be read into the .mfta file
NEW_CAP: capped prediction from PredicTM to be read into the .mfta file\n";
if (defined $porter_in){print OUTPUT_FILE "PORTER: prediction from Porter server\n"}
if (defined $apssp2_in){print OUTPUT_FILE "APSSP2: prediction from APSSP2 server\n"}
if (defined $sspro_in){print OUTPUT_FILE "SSPRO: prediction from SSPRO server\n"}
if (defined $psipred_in){print OUTPUT_FILE "PSIPRED: prediction from Psipred server\n"}
if (defined $jpred_in){print OUTPUT_FILE "JPRED: prediction from JPRED server\n"}
print OUTPUT_FILE "OLD_RAW: raw prediction from PredicTM
OLD_CAP: capped prediction from PredicTM
Predicted secondary structure: H=helix, E=strand, C=coil
Confidence: 1=lowest, 9=highest (for PSIPRED, JPRED)
Confidence: 3=lowest, *=highest (for APSSP2)

Server(s) used:
";
if (defined $porter_in){
                       print OUTPUT_FILE "PORTER: http://distill.ucd.ie/porter/\n";
                       }
if (defined $apssp2_in){
                       print OUTPUT_FILE "APSSP2: http://www.imtech.res.in/raghava/apssp2/\n";
                       }
if (defined $psipred_in){
                       print OUTPUT_FILE "PSIPRED: http://bioinf.cs.ucl.ac.uk/psipred/\n";
                        }
if (defined $sspro_in){
                       print OUTPUT_FILE "SSPRO: http://scratch.proteomics.ics.uci.edu/\n";
                        }
if (defined $jpred_in){
                       print OUTPUT_FILE "JPRED: http://www.compbio.dundee.ac.uk/www-jpred/advanced.html\n";
                        }

close OUTPUT_FILE;
exit;

sub help {
         my $help = 
"
Program:
 :: format_secondary.pl

Author:
 :: Bartosz Trzaskowski (trzask\@wag.caltech.edu)

Usage:
 :: format_secondary.pl -m {mfta} -e {expasy number} -p {porter} -a {apssp2} -j {jpred} -s {sspro} -d {psipred} -o {output}

Description:
 :: This script takes an mfta file or expasy accession
 :: number and secondary structure predictions from Porter,
 :: APSSP2, PSIPRED or SSPRO servers (either one, two, three,
 :: or all four) and formats the output to be easy readable.
 :: Also adds PredicTM raw and cap regions (from .mfta file).
 ::
 :: For a complete description check:
 :: https://wiki.wag.caltech.edu/twiki/bin/view/Biogroup/Secondary_Page
 ::
 :: Default usage:
 ::
 :: format_secondary.pl -m {mfta} -p {porter} -a {apssp2} -j {jpred}
 ::
";         
         die "$help";
         }
       
