#!/bin/octave
%plot frequency response of transfer function


function out = bode(w)
  s = i*w;
  out = 1./(s+1);
endfunction

f = linspace(0,10,1000)
w = 2*pi*f

hold on
plot(f,bode(w))
xlabel('Frequency Hz')
ylabel('Gain')

pause
