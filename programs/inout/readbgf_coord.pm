# "package" gives the namespace the module will reside in and also
# dictates the name of the file if you want it to be "use"d.

package inout::readbgf_coord;

use strict;
use warnings;
use POSIX qw(ceil floor);

our $VERSION = '1.00';

use base 'Exporter';

our @EXPORT = qw(readbgf_coord);

# define the function readbgf_coord()

sub readbgf_coord {

    my ($bgffilesub,$helixhpc) = @_;
    my $helixhpc1=floor($helixhpc);
    my $helixhpc2=$helixhpc1+1;

    open (BGF, "<$bgffilesub");
    my @bgf = <BGF>;
    close (BGF);

    my $num_bbatoms=0;
    my $num_allatoms=0;
    my $hpcanchor1=0;
    my $hpcanchor2=0;
    my @allatom_x=();
    my @allatom_y=();
    my @allatom_z=();
    my @bbatom_mass=();
    my @bbatom_x=();
    my @bbatom_y=();
    my @bbatom_z=();

    foreach my $bgfline (@bgf)
    {
        if ($bgfline =~ /ATOM/ | $bgfline =~ /HETATM/ && $bgfline !~ /FORMAT/)
        {
            $num_allatoms++;
            my ($het,$atno,$atom,$res,$chn,$resno,$xb,$yb,$zb,$fftype,$con,$ep,$chrg) = split /\ +/, $bgfline;
            $allatom_x[$num_allatoms-1] = $xb;
            $allatom_y[$num_allatoms-1] = $yb;
            $allatom_z[$num_allatoms-1] = $zb;
            if ($bgfline =~ / CA / | $bgfline =~ / C /)
            {
                $num_bbatoms++;
                $bbatom_mass[$num_bbatoms-1] = 12.0107;
                my ($het,$atno,$atom,$res,$chn,$resno,$xb,$yb,$zb,$fftype,$con,$ep,$chrg) = split /\ +/, $bgfline;
                if ($resno == $helixhpc1 && $bgfline =~ / CA /) {
                   $hpcanchor1=$num_bbatoms-1;
                }
                if ($resno =~ $helixhpc2 && $bgfline =~ / CA /) {
                   $hpcanchor2=$num_bbatoms-1;
                }
                $bbatom_x[$num_bbatoms-1] = $xb;
                $bbatom_y[$num_bbatoms-1] = $yb;
                $bbatom_z[$num_bbatoms-1] = $zb;
            } 
            elsif ($bgfline =~ / N /) 
            {
                $num_bbatoms++;
                $bbatom_mass[$num_bbatoms-1] = 14.0067;
                my ($het,$atno,$atom,$res,$chn,$resno,$xb,$yb,$zb,$fftype,$con,$ep,$chrg) = split /\ +/, $bgfline;
                $bbatom_x[$num_bbatoms-1] = $xb;
                $bbatom_y[$num_bbatoms-1] = $yb;
                $bbatom_z[$num_bbatoms-1] = $zb;
            }
        }
    }
    return ($num_allatoms,\@allatom_x,\@allatom_y,\@allatom_z,$num_bbatoms,\@bbatom_mass,\@bbatom_x,\@bbatom_y,\@bbatom_z,$hpcanchor1,$hpcanchor2);
}

=head1 AUTHOR

Ravi Abrol <abrol@wag.caltech.edu>

=cut

# A Perl module must end with a true value or else it is considered not to
# have loaded.  By convention this value is usually 1 though it can be
# any true value.  A module can end with false to indicate failure but
# this is rarely used and it would instead die() (exit with an error).

1;
