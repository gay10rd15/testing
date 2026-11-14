#!/usr/bin/perl

use warnings;
use strict;
use feature ':5.10';

my $b = "son";
my @months = ("july", "august");

@months[1] = "march";

say "hi $b";
say "@months";
