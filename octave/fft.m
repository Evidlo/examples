% Evan Widloski - 2016-02-06
% fft plotting, convolution, and filters


%Tune in to a AMDSB radio channel

sample_rate = 44100; %samples/sec
duration = 8; %sec
t = linspace(-duration/2,duration/2,sample_rate*duration)';

%----------- basic FFT --------------

x1 = sin(2*pi*1000.*t);

%plot fft of signal
subplot(3,1,1)
fftplot(x1,sample_rate,duration)
title('original')

%----------- shifting signal ------------
x2 = x1 .* 2.*cos(2*pi*100.*t);
subplot(3,1,2)
fftplot(x2,sample_rate,duration)
title('shifted signal')

%---------- lowpass ------------
filter = sin(2*pi*1000.*t)./(pi.*t);

convolved = fftconv(x2,filter);
%audio is now (x2+filter) long, we need to trim it so that it is x1 long
%get center chunk of returned sound, width = duration
convolved = convolved(ceil((length(convolved) - sample_rate*duration)/2):floor((length(convolved) + sample_rate*duration)/2),:);
%normalize sound
convolved = convolved./max(convolved);

subplot(3,1,3)
fftplot(convolved,sample_rate,duration)
title('lowpass')
pause
