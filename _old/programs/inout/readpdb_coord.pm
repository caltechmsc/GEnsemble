package inout::readpdb_coord;

use strict;
use warnings;
use POSIX qw(ceil floor);

our $VERSION = '1.00';

use base 'Exporter';

our @EXPORT = qw(readpdb_coord);

# define the function readpdb_coord()

sub readpdb_coord {

    my ($pdbfile,$begintm,$endtm,$nter,$zout) = @_;

    open (PDB, "<$pdbfile");
    my @pdb = <PDB>;
    close (PDB);

    my $num_bbatoms=0;
    my $num_allatoms=0;
    my @allatom_x=();
    my @allatom_y=();
    my @allatom_z=();
    my @bbatom_mass=();
    my @bbatom_x=();
    my @bbatom_y=();
    my @bbatom_z=();
    my $flip=1;

    foreach my $pdbline (@pdb) {
        chomp($pdbline);
        if ($pdbline =~ /ATOM/) {
        my $zb = substr $pdbline, 46, 8;
        if ($zb < 0.0) {
            if (($nter eq 'out') and ($zout eq 'plus')) {
                $flip = -1;
            } elsif (($nter eq 'in') and ($zout eq 'minus')) {
                $flip = -1;
            }
        } else {
            if (($nter eq 'out') and ($zout eq 'minus')) {
                $flip = -1;
            } elsif (($nter eq 'in') and ($zout eq 'plus')) {
                $flip = -1;
            }
        }
        last;
        }
    }

    foreach my $pdbline (@pdb) {
    chomp($pdbline);
        if (($pdbline =~ /ATOM/ or $pdbline =~ /HETATM/) and ($pdbline !~ /FORMAT/))
        {
            $num_allatoms++;
            my $resno = substr $pdbline, 22, 4;
            my $xb = substr $pdbline, 30, 8;
            my $yb = substr $pdbline, 38, 8;
            my $zb = substr $pdbline, 46, 8;
            $allatom_x[$num_allatoms-1] = $flip*$xb;
            $allatom_y[$num_allatoms-1] = $flip*$yb;
            $allatom_z[$num_allatoms-1] = $flip*$zb;
            if ($resno >= $begintm && $resno <= $endtm) {
            if ($pdbline =~ / CA / | $pdbline =~ / C /) {
                $num_bbatoms++;
                $bbatom_mass[$num_bbatoms-1] = 12.0107;
                $bbatom_x[$num_bbatoms-1] = $flip*$xb;
                $bbatom_y[$num_bbatoms-1] = $flip*$yb;
                $bbatom_z[$num_bbatoms-1] = $flip*$zb;
            } 
            elsif ($pdbline =~ / N /) 
            {
                $num_bbatoms++;
                $bbatom_mass[$num_bbatoms-1] = 14.0067;
                $bbatom_x[$num_bbatoms-1] = $flip*$xb;
                $bbatom_y[$num_bbatoms-1] = $flip*$yb;
                $bbatom_z[$num_bbatoms-1] = $flip*$zb;
            }
            }
        }
    }
    return ($num_bbatoms,\@bbatom_mass,\@bbatom_x,\@bbatom_y,\@bbatom_z);
}


=head1 AUTHOR

Ravi Abrol <abrol@wag.caltech.edu>

=cut

# A Perl module must end with a true value or else it is considered not to
# have loaded.  By convention this value is usually 1 though it can be
# any true value.  A module can end with false to indicate failure but
# this is rarely used and it would instead die() (exit with an error).

1;
