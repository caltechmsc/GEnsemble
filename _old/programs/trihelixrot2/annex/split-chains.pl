#!/usr/bin/perl

use Getopt::Std;

getopts(':h');

use File::Basename;
use FindBin ();
use lib "$FindBin::Bin";

$sbin = $FindBin::Bin;

if ($opt_h == 1)
{die "This program takes a GPCR bgf file and starts residue renumbering for each chain and 
gives each chain a different identifier, A through G.
Usage: split-chains.pl <input bgf file> <output bgf file>
" 
}

$bgffile = $ARGV[0];
$bgffilenew = $ARGV[1];

system ("$sbin/fixchains.pl $bgffile fixed.bgf");
system ("python $sbin/renumber_residues_bgf.py fixed.bgf renum.bgf");

open(BGF, "<renum.bgf");
@bgf = <BGF>;
close(BGF);

foreach $bgfline (@bgf)
{
	if ($bgfline =~ /ATOM/ && $bgfline =~ / HC /)
	{
		($atom,$atno,$type,$res,$chain,$resno,$coord) = split /\ +/, $bgfline;
		$chno++;
		$tmresno[$chno]=$resno;
	}
}

foreach $bgfline (@bgf)
{
	$m++;
	if ($bgfline =~ /ATOM/ && $bgfline !~ /FORMAT/)
	{
		($atom,$atno,$type,$res,$chain,$resno,$coord) = split /\ +/, $bgfline;
		if ($resno <= $tmresno[1])
		{
			$newbgfline[$m] = $bgfline; 
		}
		if ($resno <= $tmresno[2] && $resno > $tmresno[1])
		{	
			$resnonew = $resno - $tmresno[1];
			$bgfline =~ s/ $chain / B /; 
			if ($resno > 9 && $resno < 100)
			{
				if ($resnonew < 10)
				{	
					$bgfline =~ s/ $resno /  $resnonew /;
				}
				if ($resnonew > 9)
				{
					$bgfline =~ s/ $resno / $resnonew /;
				}
			}
			if ($resno > 99)
			{
                                if ($resnonew < 10)
                                {
                                        $bgfline =~ s/ $resno /   $resnonew /;
                                }
                                if ($resnonew > 9)
                                {
                                        $bgfline =~ s/ $resno /  $resnonew /;
                                }
                        }
			$newbgfline[$m] = $bgfline;
		} 
		if ($resno <= $tmresno[3] && $resno > $tmresno[2])
                {
                	$resnonew = $resno - $tmresno[2];
                        $bgfline =~ s/ $chain / C /;
                        if ($resno > 9 && $resno < 100)
			{
				if ($resnonew < 10)
                        	{
                                	$bgfline =~ s/ $resno /  $resnonew /;
                        	}
                        	if ($resnonew > 9)
                        	{
                                	$bgfline =~ s/ $resno / $resnonew /;
                        	}
			}
			if ($resno > 99)
			{
                                if ($resnonew < 10)
                                {
                                        $bgfline =~ s/ $resno /   $resnonew /;
                                }
                                if ($resnonew > 9)
                                {
                                        $bgfline =~ s/ $resno /  $resnonew /;
                                }
                        }
                        $newbgfline[$m] = $bgfline;

		}
		if ($resno <= $tmresno[4] && $resno > $tmresno[3])
                {
			$resnonew = $resno - $tmresno[3];
                        $bgfline =~ s/ $chain / D /;
			if ($resno > 9 && $resno < 100)
			{
                        	if ($resnonew < 10)
                        	{
                                	$bgfline =~ s/ $resno /  $resnonew /;
                        	}
                        	if ($resnonew > 9)
                        	{
                                	$bgfline =~ s/ $resno / $resnonew /;
                        	}
			}
			if ($resno > 99)
			{
                                if ($resnonew < 10)
                                {
                                        $bgfline =~ s/ $resno /   $resnonew /;
                                }
                                if ($resnonew > 9)
                                {
                                        $bgfline =~ s/ $resno /  $resnonew /;
                                }
                        }
                        $newbgfline[$m] = $bgfline;
                }
		if ($resno <= $tmresno[5] && $resno > $tmresno[4])
                {
			$resnonew = $resno - $tmresno[4];
                        $bgfline =~ s/ $chain / E /;
			if ($resno > 9 && $resno < 100)
			{
                        	if ($resnonew < 10)
                        	{
                                	$bgfline =~ s/ $resno /  $resnonew /;
                        	}
                        	if ($resnonew > 9)
                        	{
                                	$bgfline =~ s/ $resno / $resnonew /;
                        	}
			}
			if ($resno > 99)
			{
                                if ($resnonew < 10)
                                {
                                        $bgfline =~ s/ $resno /   $resnonew /;
                                }
                                if ($resnonew > 9)
                                {
                                        $bgfline =~ s/ $resno /  $resnonew /;
                                }
                        }
                        $newbgfline[$m] = $bgfline;
                }
		if ($resno <= $tmresno[6] && $resno > $tmresno[5])
                {
			$resnonew = $resno - $tmresno[5];
                        $bgfline =~ s/ $chain / F /;
			if ($resno > 9 && $resno < 100)
                        {
				if ($resnonew < 10)
                        	{
                                	$bgfline =~ s/ $resno /  $resnonew /;
                        	}
                        	if ($resnonew > 9)
                        	{
                                	$bgfline =~ s/ $resno / $resnonew /;
                        	}
			}
			if ($resno > 99)
			{
                                if ($resnonew < 10)
                                {
                                        $bgfline =~ s/ $resno /   $resnonew /;
                                }
                                if ($resnonew > 9)
                                {
                                        $bgfline =~ s/ $resno /  $resnonew /;
                                }
                        }
                        $newbgfline[$m] = $bgfline;
                }
		if ($resno <= $tmresno[7] && $resno > $tmresno[6])
                {
			$resnonew = $resno - $tmresno[6];
                        $bgfline =~ s/ $chain / G /;
			if ($resno > 9 && $resno < 100)
                        {
				if ($resnonew < 10)
                        	{
                                	$bgfline =~ s/ $resno /  $resnonew /;
                        	}
                        	if ($resnonew > 9)
                        	{
                                	$bgfline =~ s/ $resno / $resnonew /;
                        	}
			}
			if ($resno > 99)
			{
                                if ($resnonew < 10)
                                {
                                        $bgfline =~ s/ $resno /   $resnonew /;
                                }
                                if ($resnonew > 9)
                                {
                                        $bgfline =~ s/ $resno /  $resnonew /;
                                }
                        }
                        $newbgfline[$m] = $bgfline;
                }
	}
	else
	{
		$newbgfline[$m] = $bgfline;
	}
}

open (BGFNEW, ">$bgffilenew");

for ($j = 1; $j < $m+1; $j++)
{
	print BGFNEW "$newbgfline[$j]";
}

system ("rm -f renum.bgf fixed.bgf");
