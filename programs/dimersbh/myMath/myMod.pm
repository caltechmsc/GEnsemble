package myMath::myMod;

use strict;
use warnings;

our $VERSION = '1.00';

use base 'Exporter';

our @EXPORT = qw(myMod);


sub myMod {
    my ($a, $b) = @_;
    my $div  = $a / $b;
    return $a - int($div)*$b;
}

1;
