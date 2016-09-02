#!/usr/bin/octave
% Evan Widloskii
% Root Locus Example - 2016-03-09

%        K(s^2 + 2s + 2))
% G(s) = ---------------
%            s(s-2)

num = [1 2 2];
den = [1 -2 0];

system = tf(num,den);
rlocus(system);
