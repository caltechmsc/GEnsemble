package inout::readpdb_bbcoord;

use strict;
use warnings;
use POSIX qw(ceil floor);

our $VERSION = '1.00';

use base 'Exporter';

our @EXPORT = qw(readpdb_bbcoord);

# define the function readpdb_bbcoord()

sub readpdb_bbcoord {

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
    my @bbatom_resid=();
    my @bbatom_name=();
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

    my $castr = "CA";
    my $cstr = "C";
    my $nstr = "N";

    foreach my $pdbline (@pdb) {
    chomp($pdbline);
        if (($pdbline =~ /ATOM/ or $pdbline =~ /HETATM/) and ($pdbline !~ /FORMAT/))
        {
            $num_allatoms++;
            my $atomname = substr $pdbline, 12, 4;
            $atomname =~ s/^\s+//;
            $atomname =~ s/\s+$//;
            my $resno = substr $pdbline, 22, 4;
            my $xb = substr $pdbline, 30, 8;
            my $yb = substr $pdbline, 38, 8;
            my $zb = substr $pdbline, 46, 8;
            $allatom_x[$num_allatoms-1] = $xb;
            $allatom_y[$num_allatoms-1] = $flip*$yb;
            $allatom_z[$num_allatoms-1] = $flip*$zb;
            if ($resno >= $begintm && $resno <= $endtm) {
            if ($atomname eq $castr) {
                $num_bbatoms++;
                $bbatom_mass[$num_bbatoms-1] = 12.0107;
                $bbatom_x[$num_bbatoms-1] = $xb;
                $bbatom_y[$num_bbatoms-1] = $flip*$yb;
                $bbatom_z[$num_bbatoms-1] = $flip*$zb;
                $bbatom_resid[$num_bbatoms-1] = $resno;
                $bbatom_name[$num_bbatoms-1] = "CA";
            }
            elsif ($atomname eq $cstr) {
                $num_bbatoms++;
                $bbatom_mass[$num_bbatoms-1] = 12.0107;
                $bbatom_x[$num_bbatoms-1] = $xb;
                $bbatom_y[$num_bbatoms-1] = $flip*$yb;
                $bbatom_z[$num_bbatoms-1] = $flip*$zb;
                $bbatom_resid[$num_bbatoms-1] = $resno;
                $bbatom_name[$num_bbatoms-1] = "C ";
            } 
            elsif ($atomname eq $nstr) {
                $num_bbatoms++;
                $bbatom_mass[$num_bbatoms-1] = 14.0067;
                $bbatom_x[$num_bbatoms-1] = $xb;
                $bbatom_y[$num_bbatoms-1] = $flip*$yb;
                $bbatom_z[$num_bbatoms-1] = $flip*$zb;
                $bbatom_resid[$num_bbatoms-1] = $resno;
                $bbatom_name[$num_bbatoms-1] = "N ";
            }
            }
        }
    }
#   my $i = 0;
#   for ($i=0;$i < $num_bbatoms;$i++) {
#   print "$bbatom_mass[$i], $bbatom_x[$i], $bbatom_y[$i], $bbatom_z[$i]\n";
#   }
    return ($num_bbatoms,\@bbatom_mass,\@bbatom_x,\@bbatom_y,\@bbatom_z,\@bbatom_resid,\@bbatom_name);
}


=head1 AUTHOR

Ravi Abrol <abrol@wag.caltech.edu>

=cut

# A Perl module must end with a true value or else it is considered not to
# have loaded.  By convention this value is usually 1 though it can be
# any true value.  A module can end with false to indicate failure but
# this is rarely used and it would instead die() (exit with an error).

1;
