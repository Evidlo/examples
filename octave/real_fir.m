%% compare difference between symmetric/asymmetric FIR

order = 10;
n = [0 1:order];
co = .5; # normalized cutoff frequency


p = round((order/2)*co) # number of coefficients in passband
q = order - 2*p # number of coefficients in stopband

## -------------- Symmetric LPF ----------------
## create LPF sequence: [1 1 ... 1 0 ... 0 1 ... 1]
##                         |--p--|         |--p--|
lpf_k = [1 ones(1,p) zeros(1,q) ones(1,p)];
lpf_n = ifft(lpf_k);

subplot(4,1,1)
plot(n,lpf_k,'bo-')
grid on
title('Symmetric FIR Response')
subplot(4,1,2)
plot(n,real(lpf_n),'ro-',n,imag(lpf_n),'bo-')
grid on
legend('real','imaginary')
title('Symmetric FIR Coefficients')

## -------------- Asymmetric LPF ----------------
## create LPF sequence: [1 1 ... 1 0 ...  0]
##                         |--p--|
lpf_k = [1 ones(1,p) zeros(1,q + p)];
lpf_n = ifft(lpf_k);

subplot(4,1,3)
plot(n,lpf_k,'bo-')
grid on
title('Asymmetric FIR Response')
subplot(4,1,4)
plot(n,real(lpf_n),'ro-',n,imag(lpf_n),'bo-')
grid on
legend('real','imaginary')
title('Asymmetric FIR Coefficients')
