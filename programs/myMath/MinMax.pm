package myMath::MinMax;

use strict;
use warnings;

our $VERSION = '1.00';

use base 'Exporter';

our @EXPORT = qw(argmax argmin);


sub argmax(&@) {
    my $index = undef;
    my $max   = undef;
    my $block = shift;
    my $i = -1;
    for (@_) {
         my $val = $block->($_);
         $i++;
         if ( not defined $max or $val > $max ) {
             $max   = $val;
             $index = $i;
         }
    }
    return wantarray ? ($index, $max) : $index;
}

sub argmin(&@) {
    my $index = undef;
    my $min   = undef;
    my $block = shift;
    my $i = -1;
    for (@_) {
         my $val = $block->($_);
         $i++;
         if ( not defined $min or $val < $min ) {
             $min   = $val;
             $index = $i;
         }
    }
    return wantarray ? ($index, $min) : $index;
}
