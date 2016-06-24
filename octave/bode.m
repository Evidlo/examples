#!/bin/octave
%plot frequency response of transfer function

## Vi  o----- sL ------o Vo
##       |         |
##       |        1/sC
##       |         |
## Gnd o----- R -------o

##              (R/L)s + 1/(LC)
## Vo/Vi =   ---------------------
##           s^2 + (R/L)s + 1/(LC)


pkg load control

R=1;
L=1;
C=1;

system = tf([R/L 1/(L*C)],[1 R/L 1/(L*C)])

subplot(2,1,1)
bode(system)
xlabel('Frequency Hz')
ylabel('Gain')

subplot(2,1,1)
t = linspace(0,100,10000);
y = sin(t);
lsim(sys,y,t)
