#!/usr/local/bin/perl -w

for $n (1..50) {
    if ($n <= 9) {
	$n = "0" . $n;
    }
    
    system("cp P.lib P_${n}-charge-corrected.lib");
    system("perl -p -i -e 's/name SCWRL/name $n/' P_${n}-charge-corrected.lib");

}
