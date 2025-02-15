#!/bin/bash

export GE_PATH="/groups/wag/GEnsemble"
export PATH="$GE_PATH/programs:$PATH"

alias ge_blast="$GE_PATH/programs/Blast.pl"
alias ge_predictm="$GE_PATH/programs/PredicTM.pl"
alias ge_opthelix="$GE_PATH/programs/OptHelix.pl"
alias ge_template="$GE_PATH/programs/Align2Template.pl"
alias ge_bihelix="$GE_PATH/programs/bihelixrot2/all_bihelix_pairs.pl"
alias ge_bihelixanal="$GE_PATH/programs/bihelixrot2/bihelix_anal.pl"
alias ge_combihelix="$GE_PATH/programs/bihelixrot2/combi_frombihelixsum.pl"
