#!/usr/local/bin/perl -w

use strict;

my $AA = "A";
for my $n (1..9) {
    #system("perl -p -i -e 's/REM library_name SCWRL/REM library_name 0$n/' 
    system("cp ${AA}_0${n}-charge-corrected.lib ${AA}_0${n}-libname-corrected.lib");
    system("perl -p -i -e 's/REM library_name SCWRL/REM library_name 0$n/' ${AA}_0${n}-libname-corrected.lib");
    system("ln -sf ${AA}_0${n}-libname-corrected.lib ${AA}_0${n}.lib");


}

for my $n (10..50) {
    print $n, "\n";
    system("cp ${AA}_${n}-charge-corrected.lib ${AA}_${n}-libname-corrected.lib");
    system("perl -p -i -e 's/REM library_name SCWRL/REM library_name $n/' ${AA}_${n}-libname-corrected.lib");
    system("ln -sf ${AA}_${n}-libname-corrected.lib ${AA}_${n}.lib");

}
