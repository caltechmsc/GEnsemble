#!/usr/bin/perl -w

($duration) = @ARGV if (@ARGV);
die "Converts time in seconds to common time units\n$0 <elapsed-time-in-seconds>\n\n" unless (defined $duration && $duration =~ /^[0-9]+$/);

# calculate

$sec = $duration % 60;
$duration = ($duration - $sec) / 60;

if ($duration) {
    $min = $duration % 60;
    $duration = ($duration - $min) / 60;
}

if ($duration) {
    $hour = $duration % 24;
    $duration = ($duration - $hour) / 24;
}

if ($duration) {
    $day = $duration;
}

# print
#print "\n";
print " $day days," if ($day);
print " $hour hrs," if ($hour);
print " $min min," if ($min);
print " $sec sec\n";

exit;
