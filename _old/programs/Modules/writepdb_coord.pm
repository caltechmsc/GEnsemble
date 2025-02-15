# "package" gives the namespace the module will reside in and also
# dictates the name of the file if you want it to be "use"d.

package Modules::writepdb_coord;

use strict;
use warnings;
use POSIX qw(ceil floor);

our $VERSION = '1.00';

use base 'Exporter';

our @EXPORT = qw(writepdb_coord);

# define the function writepdb_coord()

sub writepdb_coord {

    my ($inputpdb,$outputpdb,$allatom_x_ref,$allatom_y_ref,$allatom_z_ref) = @_;

    my @x=@$allatom_x_ref;
    my @y=@$allatom_y_ref;
    my @z=@$allatom_z_ref;

    open (IBGF, "<$inputbgf");
    open (OBGF, ">$outputbgf");
    my @bgf = <IBGF>;
    close (IBGF);

    my $j=-1;
    foreach my $bgfline (@bgf) {
        if ($bgfline =~ /ATOM/ | $bgfline =~ /HETATM/ && $bgfline !~ /FORMAT/) {
            $j++;
            my $prefixline = substr($bgfline,0,30);
            my $suffixline = substr($bgfline,60);

            my $xxb = sprintf("%10.5f", $x[$j]);
            my $yyb = sprintf("%10.5f", $y[$j]);
            my $zzb = sprintf("%10.5f", $z[$j]);

            print OBGF "$prefixline$xxb$yyb$zzb$suffixline";
        } else {
            print OBGF "$bgfline";
        }
    }
    close (OBGF);
}

=head1 AUTHOR

Ravi Abrol <abrol@wag.caltech.edu>

=cut

# A Perl module must end with a true value or else it is considered not to
# have loaded.  By convention this value is usually 1 though it can be
# any true value.  A module can end with false to indicate failure but
# this is rarely used and it would instead die() (exit with an error).

1;
