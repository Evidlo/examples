% Evan Widloski - 2016-02-06
% fft plotting, convolution, and filters


%Tune in to a AMDSB radio channel

sample_rate = 8000;
duration = 1;
n = 1:sample_rate*duration;

## define discrete time signal
x1 = cos(2*pi*1000.*n/sample_rate);

## define values for x axis
frequencies = linspace(-sample_rate/2,sample_rate/2,sample_rate*duration);

plot(frequencies,real(fftshift(fft(x1))))
axis([min(frequencies) max(frequencies)])
%----------- basic FFT --------------


%plot fft of signal
title('original')

%----------- shifting signal ------------
## x2 = x1 .* 2.*cos(2*pi*100.*t);
## subplot(3,1,2)
## fftplot(x2,sample_rate,duration)
## title('shifted signal')

## %---------- lowpass ------------
## filter = sin(2*pi*1000.*t)./(pi.*t);

## convolved = fftconv(x2,filter);
## %audio is now (x2+filter) long, we need to trim it so that it is x1 long
## %get center chunk of returned sound, width = duration
## convolved = convolved(ceil((length(convolved) - sample_rate*duration)/2):floor((length(convolved) + sample_rate*duration)/2),:);
## %normalize sound
## convolved = convolved./max(convolved);

## subplot(3,1,3)
## fftplot(convolved,sample_rate,duration)
## title('lowpass')
## pause
