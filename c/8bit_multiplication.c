// Evan Widloski - 2016-11-05
// Test multiplication of binary fractions

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

// convert byte to binary string for display purposes
// stolen from http://stackoverflow.com/questions/111928/is-there-a-printf-converter-to-print-in-binary-format
const char *byte_to_binary(int x)
{
  static char b[9];
  b[0] = '\0';

  int z;
  for (z = 128; z > 0; z >>= 1)
    {
      strcat(b, ((x & z) == z) ? "1" : "0");
    }

  return b;
}

void main(){

  int8_t a, b, result;

  // When multiplying binary fractions, the ints should first be cast to
  // larger integers before multiplying, then bitshift to remove insignificant bits

  // ((int16_t)a*(int16_t)b)>>7

  //  ---------- Precision Tests ------------


  // smallest fraction that can be held in 8-bit int is 1/128
  // (a/128)*(b/128) > 1/128 --> (a*b) > 128

  //so (11/128)*(12/128) should yield a nonzero value
  a = 0b00001011;
  b = 0b00001100;

  result = ((int16_t)a*(int16_t)b)>>7;
  printf("(11/128)*(12/128):%s\n",byte_to_binary(result));

  // and (11/128)*(11/128) should yield a zero value
  a = 0b00001011;
  b = 0b00001011;

  result = ((int16_t)a*(int16_t)b)>>7;
  printf("(11/128)*(11/128):%s\n",byte_to_binary(result));

  // ---------- Overflow Tests ------------

  // signed 8-bit int can hold fractional values in the range [-1,1), (radix)

  // (-128/128)*(-128/128) should overflow and return -1
  a = 0b10000000;
  b = 0b10000000;

  result = ((int16_t)a*(int16_t)b)>>7;
  printf("(-128/128)*(-128/128):%s\n",byte_to_binary(result));

  // (-128/128)*(127/128) should return -127/128
  a = 0b10000000;
  b = 0b01111111;

  result = ((int16_t)a*(int16_t)b)>>7;
  printf("(-128/128)*(127/128):%s\n",byte_to_binary(result));

}
