#!/bin/octave
## Evan Widloski - 2016-07-14
## DFT Testing - practicing and understanding inverse DFT

duration = 1;
sample_freq = 25;

N = duration*sample_freq;

n = 0:N-1;

x_time = sin(2*pi*1*n/N) + cos(2*pi*5*n/N);
x = [0 -12.5i 0 0 0 12.5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12.5 0 0 0 12.5i];

## show original signal
subplot(6,1,1)
plot(n,x_time)
grid on
title(sprintf('Original Signal - Time Domain'))

## show original signal DFT components
subplot(6,1,2)
plot(n,real(x),'r',n,imag(x),'g')
grid on
legend('Real','Imaginary')
title(sprintf('Original Signal - DFT Components'))

## perform inverse discrete fourier transform using cos and sin components
out=zeros(1,N);
for k = n
  c = cos((2*pi*k*n)/N);
  s = sin((2*pi*k*n)/N);
  out += x(k+1)*(c + i*s);
endfor

out = (1/N)*out;

## show result of inverse DFT
subplot(6,1,3)
plot(n,real(out),'k')
grid on
title(sprintf('Inverse DFT - Real Components'))
subplot(6,1,4)
plot(n,imag(out),'k')
grid on
title(sprintf('Inverse DFT - Imaginary Components'))

## plot IFFT for comparison
subplot(6,1,5)
plot(n,real(ifft(x)))
grid on
title('IFFT Result - Real Components')
subplot(6,1,6)
plot(n,imag(ifft(x)))
grid on
title('IFFT Result - Imaginary Components')
