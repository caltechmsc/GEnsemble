#!/usr/bin/perl
use POSIX;

$tm1 = @ARGV[0];
$tm2 = @ARGV[1];
$nm = @ARGV[2];
$lst = @ARGV[3];
$anal = @ARGV[4];

if ($tm1 == 1 && $tm2 == 2)
{
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_bihelix_anal/super_anal1 $anal");
}

if ($tm1 == 1 && $tm2 == 7)
{
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_bihelix_anal/super_anal2 $anal");
}

if ($tm1 == 2 && $tm2 == 3)
{
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_bihelix_anal/super_anal3 $anal");
}

$d1 = 0;
while ($d1 < 1)
{
  if (-e 'Total_Energy_1_temp')
  {$d1++;}
}

$d2 = 0;
while ($d2 < 1)
{
  if (-e 'Total_Energy_2_temp')
  {$d2++;}
}

$d3 = 0;
while ($d3 < 1)
{
  if (-e 'Total_Energy_3_temp')
  {$d3++;}
}

if ($tm1 == 1 && $tm2 == 2)
{
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_bihelix_anal/super_anal_sort2 $anal");
}

$d4 = 0;
while ($d4 < 1)
{
  if (-e 'Consensus_7.out')
  {$d4++;}
}

if ($tm1 == 2 && $tm2 == 3)
{
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/output_TM_configs");
}

open (TM1,"<Consensus_1.out");
@tm1 = <TM1>;
close (TM1);
$size = @tm1;

if ($size > 48)
{
  $size2 = 12;
  $numb = 4;
}
if ($size > 36 && $size <= 48)
{
  $size2 = ceil($size/4);
  $numb = 4;
}
if ($numb == 4 && $nm == 2)
{
  $size2 = 12;
  $numb = 3;
}
if ($size > 24 && $size <= 36)
{
  $size2 = ceil($size/3);
  $numb = 3;
}
if ($numb == 3 && $nm == 1)
{
  $size2 = 12;
  $numb = 2;
}
if ($size > 12 && $size <= 24)
{
  $size2 = ceil($size/2);
  $numb = 2;
}
if ($size <= 12)
{
  $size2 = $size;
  $numb = 1;
}

if ($tm1 == 1 && $tm2 == 2) 
{
  $proc = 1;
}
if ($tm1 == 1 && $tm2 == 7) 
{
  $proc = 2;
}
if ($tm1 == 2 && $tm2 == 3) 
{
  $proc = 3;
}
if ($tm1 == 2 && $tm2 == 4) 
{
  $proc = 4;
}
if ($tm1 == 2 && $tm2 == 7) 
{
  $proc = 5;
}
if ($tm1 == 3 && $tm2 == 4) 
{
  $proc = 6;
}
if ($tm1 == 3 && $tm2 == 5) 
{
  $proc = 7;
}
if ($tm1 == 3 && $tm2 == 6) 
{
  $proc = 8;
}
if ($tm1 == 3 && $tm2 == 7) 
{
  $proc = 9;
}
if ($tm1 == 4 && $tm2 == 5) 
{
  $proc = 10;
}
if ($tm1 == 5 && $tm2 == 6) 
{
  $proc = 11;
}
if ($tm1 == 6 && $tm2 == 7) 
{
  $proc = 12;
}

if ($proc <= $size2)
{
  if ($proc < $size2)
  {
    $final = 0;
  }
  if ($proc == $size2)
  {
    $final = 1;
  } 
  system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/super_bihelix_anal/mean_field_anal $proc $numb $nm $final $lst");
}
