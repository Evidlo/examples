#!/bin/octave
## Evan Widloski - 2016-10-15
## convert `x` to `n`-bit signed binary fraction, expressed as an `n`-bit decimal

function out = dec2binfrac(x,n)
  ## round input array to nearest 1/(2^n)
  x = round(x * 2^n)/(2^n);
  k = [1:n-1];
  if (x < 0)
    x = 1+x;
    out = -2^(n-1);
  else
    out = 0;
  endif
  twos_complement = mod(abs(x),.5.^(k-1)) >= .5.^k;
  bin_values = 2.^[n-2:-1:0];
  out += sum(bin_values .* twos_complement);
endfunction
