#!/usr/bin/perl
# Jenelle Bray (jenelle@caltech.edu)  11 May 2007
# Ravi Abrol (abrol@wag.caltech.edu)  12 May 2007

$bgf = $ARGV[0];
$pdb = $ARGV[1];
$out = $ARGV[2];

if ($bgf !~ /bgf/ | $pdb !~ /pdb/ | $out !~ /bgf/)
{die "\nmapxyz_pdb2bgf.pl copies the coordinates from a pdb file into a template bgf file to create a new bgf file with the coordinates from the pdb file.  The atom ordering must be the identical in the pdb and bgf files.

Usage: mapxyz_pdb2bgf.pl <template_bgf_file> <pdb_file> <output_bgf_file>\n
"} 

open (BGF, "<$bgf");
@bgf = <BGF>;
close (BGF);

open (PDB, "<$pdb");
@pdb = <PDB>;
close (PDB);

open (OUT, ">$out");

$i = 0;
foreach $pdbline (@pdb)
{
	if ($pdbline =~ /ATOM/ | $pdbline =~ /HETATM/)
	{
	$i++;	
		($het,$atno,$atom,$res,$chn,$resno,$xxp,$yyp,$zzp) = split /\ +/, $pdbline;
	$xxp[$i] = sprintf("%.5f", $xxp);
	$yyp[$i] = sprintf("%.5f", $yyp);
	$zzp[$i] = sprintf("%.5f", $zzp);
	}
}

$j = 0;
foreach $bgfline (@bgf)
{
	if ($bgfline =~ /ATOM/ | $bgfline =~ /HETATM/ && $bgfline !~ /FORMAT/)
	{
    	$j++;
        $prefixline = substr($bgfline,0,30);
        $suffixline = substr($bgfline,60);
#
        $xxb = sprintf("%10.5f", $xxp[$j]);
        $yyb = sprintf("%10.5f", $yyp[$j]);
        $zzb = sprintf("%10.5f", $zzp[$j]);
# 
    	print OUT "$prefixline$xxb$yyb$zzb$suffixline";
	}
    else
    {
    	print OUT "$bgfline";
    }
}

close (OUT);
