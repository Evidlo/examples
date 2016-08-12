// Evan Widloski - 2016-08-12
// testing fixed point multiplication of signed 16bit ints
// note that adc_hist is initialized to 0, then 0x8000 is stuffed in
// this will show us the step response of the filter, which should just be a linear increase from 0x0000 to 0x8000

#include <stdint.h>
#include <stdio.h>

void main(){
  int16_t coeffs[4] = {
    32768 * .25,
    32768 * .25,
    32768 * .25,
    32768 * .25,
  };

  // create 4 position circular buffer
  int16_t adc_hist[4] = {0,0,0,0};

  // buffer pointer
  int head = 0;
  // sentry variable
  int i = 0;
  // product of fixed point multiplication
  int16_t product = 0;
  // result of 1 iteration of filter
  int16_t result = 0;

  while (1){
    // 0x8000 = 32768, this is the maximum value of a signed 16bit int
    adc_hist[head] = 0x8000;

    result = 0;
    for(i = 0; i < 4; i++){
      product = (((int32_t)adc_hist[(head + i) % 4] * (int32_t)coeffs[i]))>>15;
      // account for rounding error? 
      /* product = (((int32_t)adc_hist[(head + i) % 4] * (int32_t)coeffs[i]) + 32768)>>15; */
      result += product;
      printf("multiplying: %hx * %hx = %hx\n",adc_hist[(head + i) % 4],coeffs[i],product);
    }
    printf("result:%hx\n",result);

    head = (head + 1) % 4;
    getchar();
  }
}
