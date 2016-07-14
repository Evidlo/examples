#!/bin/octave
## Evan Widloski - 2016-07-14
## DFT Testing - practicing and understanding DFT

duration = 1;
sample_freq = 25;

N = duration*sample_freq;

n = 0:N-1;

x = sin(2*pi*1*n/N) + cos(2*pi*5*n/N);

for k = n
  c = cos((2*pi*k*n)/N);
  s = -sin((2*pi*k*n)/N);

  ## show original signal and sin/cos to calculate correlation with
  subplot(6,1,1)
  plot(n,x,'k',c,'r',s,'g')
  legend('input','cosine','sine')
  grid on
  title(sprintf('Original Signal - k=%d',k))

  ## first step in finding correlation
  subplot(6,1,2)
  plot(n,c.*x,'r',s.*x,'g')
  grid on
  title(sprintf('Input * Sinusoid - k=%d',k))

  ## calculate correlation by summing previous signal
  subplot(6,1,3)
  hold on
  plot(k,sum(c.*x))
  grid on
  hold off
  title('Cosine Components')

  ## calculate correlation by summing previous signal
  subplot(6,1,4)
  hold on
  plot(k,sum(s.*x))
  grid on
  hold off
  title('Sine Components')

  drawnow
endfor

## show FFT for comparison
subplot(6,1,5)
plot(n,real(fft(x)))
grid on
title('FFT Result - Real Components')
subplot(6,1,6)
plot(n,imag(fft(x)))
grid on
title('FFT Result - Imaginary Components')
