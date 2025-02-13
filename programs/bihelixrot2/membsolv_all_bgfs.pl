#!/usr/bin/perl

    use File::Basename;
    use FindBin ();
    use lib "$FindBin::Bin";

    $sbin = $FindBin::Bin;

	@bgfl = `ls *.bgf`;
	chomp @bgfl;
    $hpcfile = $ARGV[0];
#   print "$hpcfile\n";

	$bgflist = 'bgflist';
	open (BGFLIST, ">$bgflist");
 
	foreach $bgfl (@bgfl)
	{
        system ("echo starting $bgfl");
        ( $bgfp, $path, $suffix ) = fileparse( $bgfl, qr/\.[^.]*/ );
        if ($path || $suffix) {}; # Avoid warning
        system ("cp $bgfl temp1.bgf");
        system ("$sbin/annex/bgf2delphi.pl temp1.bgf");
        print "entering align to HPC plane script\n";
        system ("$sbin/annex/align_HPCplane_to_Lipid.py temp1.bgf $hpcfile");
        print "exited align to HPC plane script\n";
        $bgfpa = "$bgfp"."_malign.bgf";
        $bgflp = 'temp1-align.pdb';
        $bgfsiz = 'temp1.siz';
        $bgfcrg = 'temp1.crg';
        $bgfsizinp = 'in\(siz,file=\"'.$bgfsiz.'\"\)';
        $bgfcrginp = 'in\(crg,file=\"'.$bgfcrg.'\"\)';
        $bgfmemb5dir = $bgfp.'_memb5';
        $bgfmemb5out = $bgfmemb5dir.'_delphi.out';
        $bgfwaterdir = $bgfp.'_water';
        $bgfwaterout = $bgfwaterdir.'_delphi.out';
        $bgfnonpoldir = $bgfp.'_nonpol';
        $bgfnonpolout = $bgfnonpoldir.'.out';

        system ("mkdir $bgfmemb5dir");
        system ("mkdir $bgfwaterdir");
        system ("mkdir $bgfnonpoldir");

        system ("cat $sbin/annex/delphi/fort.13.memb5 > $bgfmemb5dir/fort.13");
        system ("grep ATOM $bgflp >> $bgfmemb5dir/fort.13");
        system ("cp $bgfsiz $bgfmemb5dir/"); 
        system ("cp $bgfcrg $bgfmemb5dir/"); 
        system ("cp $sbin/annex/delphi/delphi.params $bgfmemb5dir/");
        system ("echo $bgfsizinp >> $bgfmemb5dir/delphi.params");
        system ("echo $bgfcrginp >> $bgfmemb5dir/delphi.params");
        chdir($bgfmemb5dir);
        system ("echo running delphi on $bgfl in memb");
        system ("$sbin/annex/delphi/delphi delphi.params > $bgfmemb5out");
        system ("rm -f gmon.out");
        chdir("..");

        system ("cat $sbin/annex/delphi/fort.13.water > $bgfwaterdir/fort.13");
        system ("grep ATOM $bgflp >> $bgfwaterdir/fort.13");
        system ("cp $bgfsiz $bgfwaterdir/");
        system ("cp $bgfcrg $bgfwaterdir/");
        system ("cp $sbin/annex/delphi/delphi.params $bgfwaterdir/");
        system ("echo $bgfsizinp >> $bgfwaterdir/delphi.params");
        system ("echo $bgfcrginp >> $bgfwaterdir/delphi.params");
        chdir($bgfwaterdir);
        system ("echo running delphi on $bgfl in bulk water");
        system ("$sbin/annex/delphi/delphi delphi.params > $bgfwaterout");
        system ("rm -f gmon.out");
        chdir("..");

        system("cp temp1.bgf $bgflp $bgfnonpoldir");
        chdir($bgfnonpoldir);
        system ("echo running nonpolar solvation on $bgfl from water to memb");
        system("$sbin/annex/mapxyz_pdb2bgf.pl temp1.bgf $bgflp temp1-align.bgf");
        system("$sbin/annex/nonpolar_bgf.pl temp1-align.bgf");
        system("mv temp1-align.nonpolar.out $bgfnonpolout"); 
        system("rm -f area_*.out temp1.bgf temp1-align.pdb");
        system("$sbin/annex/add_GPCR_chains2.pl temp1-align.bgf > ../$bgfpa");
        chdir("..");
        system("rm -f temp1*");

        print BGFLIST "$bgfl\n";
	}

	close (BGFLIST);
