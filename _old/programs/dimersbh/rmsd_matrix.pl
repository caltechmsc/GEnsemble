#!/usr/bin/perl

$ref = $ARGV[0];
$bgflist = $ARGV[1];
$out = $ARGV[2];

@bgflist = `ls $bgflist`;
chomp @bgflist;

open(OUT,">$out");

($refpre,$bg) = split /\.bgf/, $ref;
$refpdb = $refpre . ".pdb";
system("/project/Biogroup/scripts/perl/bgf2pdb.pl $ref > $refpdb");

foreach $bgf (@bgflist)
{
  if ($bgf ne $ref)
  {
    ($pre,$bg) = split /\.bgf/, $bgf;
    $pdb = $pre . ".pdb";
    $file = "rmsd_out_temp";
    system("/project/Biogroup/scripts/perl/bgf2pdb.pl $bgf > $pdb");
    system("/ul/jenelle/profit/profit_matrix -f /ul/jenelle/codes/other/rmsd.script $refpdb $pdb > $file");
    open(IN,"<$file");
    @in=<IN>;
    close(IN);
    foreach $inline (@in)
    {
      if ($inline =~ /RMS:/)
      {
        ($rm,$rmsd) = split /:/, $inline;
      }
    }
    if ($rmsd <= 0.3)
    {
      $rmsd = " 0.0\n";
    }
    print OUT "$rmsd";  
    system("rm -f $file");
  }
}    

