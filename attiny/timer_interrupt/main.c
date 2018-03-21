#include <avr/io.h>
#include <avr/interrupt.h>

void main() {
    DDRB = (1<<PB1);  // set PB1 to output

    // enable timer clock and set prescaler to 1
    TCCR1 =  1<<CS10;

    // run TIMER1_COMPA interrupt when there's a match on timer 1, comparator A
    TIMSK |= 1<<OCIE1A;

    OCR1A = 255; // TOP - when to toggle OC1A
    OCR1C = 255; // when to reset TCINT1

    sei(); //enable interrupts

    while(1){}
}

ISR(TIMER1_COMPA_vect){
    PORTB ^= 1<<PB1; // toggle output
}
