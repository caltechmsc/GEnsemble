#!/usr/bin/env perl

use warnings;

use Getopt::Long;
#use LWP;
use LWP::Simple;
use LWP::UserAgent;

if (@ARGV == 0) { help(); }

GetOptions ('h|help'            => \$help,
            'e|expasy=s'        => \$expasy,
            'f|fasta=s'         => \$fasta,
            'p|porter_email'    => \$porter_email,
            'd|psipred_email'   => \$psipred_email,
            's|sspro_email'     => \$sspro_email,
            'a|apssp2_email'    => \$apssp2_email,
            'j|jpred_email'     => \$jpred_email,
            'm|email_address=s' => \$email_address,
#            'o|out=s'           => \$output,
            );

if ($help) { help(); }
if (!$expasy && !$fasta) {die "Must specify either EXPASY number or provide fasta file!\nFor Help: secondary_submit.pl -h\n\n"; }
if (!$porter_email && !$sspro_email && !$apssp2_email && !$jpred_email && !$psipred_email) { die "Must specify at least one of PORTER or SSPRO or APSSP2 or JPRED or PSIPRED!\nFor Help: secondary_submit.pl -h\n\n"; }

if (defined $expasy){
                    my $url = 
                    "http://www.uniprot.org/uniprot/"  .
                    "$expasy"  .
                    ".fasta"   ;
                   $html = get $url;
                   die "Could not load EXPASY/UNIPROT file.\n" unless defined $html;
                   open FASTA, ">$expasy.submit"; print FASTA "$html"; close FASTA;
                   }

if (defined $fasta){
                   open(FASTA, $fasta) or die "Could not open fasta file.\n";
                   while( <FASTA> ){
                        s/>.*//;
                        next if /^(\s)*$/;
                        chomp;
                        push @expasy, $_;
                        }
                   close FASTA;
                   $seq = join("",@expasy);
                   }

elsif (defined $expasy){
                    open(EXPASY, "$expasy.submit");
                    while( <EXPASY> ) {
                        s/>.*//;
                        next if /^(\s)*$/;
                        chomp;
                        push @expasy, $_;
                        }
                    close EXPASY;
                    $seq = join("",@expasy);
                    }

if (defined $fasta){$expasy = $fasta;}

if (defined $porter_email) {
                           my $url_porter =
                           "http://distillf.ucd.ie/~distill/cgi-bin/distill/predict?" .
                           "porter=secondary"  .
                           "&email_address=$email_address"  .
                           "&input_name=$expasy"  .
                           "&input_text=$seq" ;
                           $html_porter = get $url_porter;
                           open PORTER_EMAIL, ">>$expasy.submit";
                           print  "Could not submit PORTER results.\n" unless defined $html_porter;
                           open PORTER_EMAIL, ">>$expasy.submit"; 
                           print PORTER_EMAIL "\nPorter command: \n\n $url_porter \n\n";
                           print PORTER_EMAIL "**************************\n*  Porter job submitted  *\n**************************\n\n" unless not defined $html_porter; 
                           print "**************************\n*  Porter job submitted  *\n**************************\n\n" unless not defined $html_porter;
                           print PORTER_EMAIL "Could not submit PORTER prediction.\n\n" unless defined $html_porter;
                           print "Could not submit PORTER results.\n" unless defined $html_porter;
                           close PORTER_EMAIL;
                           }

if (defined $sspro_email) {
                           my $url_sspro =
                           "http://scratch.proteomics.ics.uci.edu/cgi-bin/new_server/sql_predict.cgi?"  .
                           "email=$email_address"  .
                           "&query_name=$expasy"  .
                           "&amino_acids=$seq"  .
                           "&ss=true"  ;
                           $html_sspro = get $url_sspro;
                           open SSPRO_EMAIL, ">>$expasy.submit";
                           print SSPRO_EMAIL "SSPRO command: \n\n $url_sspro \n\n";
                           print SSPRO_EMAIL "***************************\n*  SSPRO job submitted  *\n***************************\n\n" unless not defined $html_sspro;
                           print "***************************\n*  SSPRO job submitted  *\n***************************\n\n" unless not defined $html_sspro;
                           print SSPRO_EMAIL "Could not submit SSPRO prediction.\n\n" unless defined $html_sspro;
                           print "Could not submit SSPRO results.\n" unless defined $html_sspro;
                           close SSPRO_EMAIL;
                          }

if (defined $apssp2_email) {
                           my $browser_apssp2 = LWP::UserAgent->new;
                           my $url_apssp2 =
                           "http://www.imtech.res.in/cgibin/apssp2/apssp.pl?"  .
                           "target=$expasy" . 
                           "&seq=$seq"  .
                           "&Input=seq1"  .
                           "&email=$email_address"  ;
                           $html_apssp2 = $browser_apssp2->get ($url_apssp2, 'Referer' => 'http://www.imtech.res.in/raghava/apssp2/', 'User-Agent' => 'Mozilla/4.76 [en] (Win98; U)', );
                           open APSSP2_EMAIL, ">>$expasy.submit";
                           print APSSP2_EMAIL "APSSP2 command: \n\n $url_apssp2 \n\n";
                           print APSSP2_EMAIL "***************************\n*  APSSP2 job submitted  *\n***************************\n\n" unless not defined $html_apssp2;
                           print "***************************\n*  APSSP2 job submitted  *\n***************************\n\n" unless not defined $html_apssp2;
                           print APSSP2_EMAIL "Could not submit APSSP2 prediction.\n\n" unless defined $html_apssp2;
                           print "Could not submit APSSP2 results.\n" unless defined $html_apssp2;   
                           close APSSP2_EMAIL;
                          }

if (defined $jpred_email) {
                           my $url_jpred =
                           "http://www.compbio.dundee.ac.uk/www-jpred/cgi-bin/jpred_form?"  .
                           "seq=$seq" .
                           "&input=seq" .
                           "&pdb=true" .
                           "&email=$email_address"  .
                           "&queryName=$expasy"  ;
                           $html_jpred = get $url_jpred;
                           open JPRED_EMAIL, ">>$expasy.submit";
                           print JPRED_EMAIL "JPRED command: \n\n $url_jpred \n\n";
                           print JPRED_EMAIL "***************************\n*  JPRED job submitted  *\n***************************\n\n" unless not defined $html_jpred;
                           print "***************************\n*  JPRED job submitted  *\n***************************\n\n" unless not defined $html_jpred;
                           print JPRED_EMAIL "Could not submit JPRED prediction.\n\n" unless defined $html_jpred;
                           print "Could not submit JPRED results.\n" unless defined $html_jpred;
                           close JPRED_EMAIL;
                          }

if (defined $psipred_email) {
                           my $url_psipred =
                           "program=psipred"  .
                           "&sequence=$seq" .
                           "&complex=true" .
                           "&membrane=false" .
                           "&coil=false" .
                           "&email=$email_address"  .
                           "&passwd=" .
                           "&subject=$expasy"  ;
                           system("wget --referer=http://bioinf.cs.ucl.ac.uk/psipred --post-data '$url_psipred' http://bioinf.cs.ucl.ac.uk/psipred/submit");
                           open PSIPRED_EMAIL, ">>$expasy.submit";
                           print PSIPRED_EMAIL "PSIPRED command: \n\n wget --referer=http://bioinf.cs.ucl.ac.uk/psipred --post-data '$url_psipred' http://bioinf.cs.ucl.ac.uk/psipred/submit\n\n";
                           print PSIPRED_EMAIL "*************************\n*  PSIPRED job submitted  *\n*************************\n\n";
                           print "*************************\n*  PSIPRED job submitted  *\n*************************\n\n";
                           close PSIPRED_EMAIL;
                          }

#if (!$output) { $output = "$expasy.submit"; }
#open ADD_EMAIL, ">>$expasy.submit";
#print ADD_EMAIL "\nTo submit the PSIPRED job (not required) go to http://bioinf.cs.ucl.ac.uk/psipred/\nand enter Your email address and protein sequence.\n";

unlink("submit");

exit;

sub help {
         my $help = 
"
Program:
 :: secondary_submit.pl

Author:
 :: Bartosz Trzaskowski (trzask\@wag.caltech.edu)

Usage:
 :: secondary_submit.pl -e {expasy number} -f {fasta file} -p {porter} -s {sspro} -a {apssp2} -j {jpred} -d {psipred} -m {email_address} -o {output}

Description:
 :: This script takes the expasy accession number and
 :: submits secondary structure prediction jobs at Porter
 :: and/or APSSP2 and/or SSPRO and/or JPRED and/or PSIPRED
 :: servers. The predictions are sent as email messages to
 :: the specified email address.
 ::
 :: For a complete description check: 
 :: https://wiki.wag.caltech.edu/twiki/bin/view/Biogroup/Secondary_Page
 ::
 :: Default usage:
 ::
 :: secondary_submit.pl -e {expasy number} -p -a -j -m {email_address}
 ::
";         
         die "$help";
         }

