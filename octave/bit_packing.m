#!/bin/octave
## Evan Widloski - 2016-10-25
## Figuring out how to efficiently pack oddly sized data

## Variable:              x            y            z
## Possible values:  (0, X - 1)   (0, Y - 1)   (0, Z - 1)
##
##        encoded =      xYZ    +     yZ     +     Z
##
## Decoding:
##        z = (A % Z)/1
##        y = (A % YZ)/Z
##        x = (A % XYZ)/YZ
##
##
##    bits required without bit stuffing ceil(log2(X))+ceil(log2(Y))+ceil(log2(Z))
##    bits required with bit stuffing ceil(log2(X*Y*Z))

## possible number of states for each variable
X = 3;
Y = 3;
Z = 3;

## generate a random X, Y and Z
x = randi([0 X - 1],1,1);
y = randi([0 Y - 1],1,1);
z = randi([0 Z - 1],1,1);

## encode X,Y,Z as a single number
encoded =   x * Y * Z ...
          + y * Z ...
          + z;

printf("xyz: %d%d%d\n",x,y,z);
printf("Encoded Decimal Value: %d\n",encoded);
printf("Binary representation: %s\n",dec2bin(encoded));

z = floor(mod(encoded,Z)/1);
y = floor(mod(encoded,Y*Z)/Z);
x = floor(mod(encoded,X*Y*Z)/(Y*Z));

printf("Recovered xyz: %d%d%d\n",x,y,z);
