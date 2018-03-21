DEVICE     = attiny85
CLOCK      = 8000000
PROGRAMMER = usbasp
PORT	  	 = /dev/arduino
BAUD       = 19200
FILE    	 = main
COMPILE    = avr-gcc -Wall -Os -DF_CPU=$(CLOCK) -mmcu=$(DEVICE)

all: build upload

8mhz-internal:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -U lfuse:w:0x42:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m

1mhz-internal:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -U lfuse:w:0x62:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m

8mhz-external:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -U lfuse:w:0x6e:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m

16mhz-external:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -U lfuse:w:0xfe:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m

build:
	$(COMPILE) -c $(FILE).c -o $(FILE).o
	$(COMPILE) -o $(FILE).elf $(FILE).o
	avr-objcopy -j .text -j .data -O ihex $(FILE).elf $(FILE).hex
	avr-size --format=avr --mcu=$(DEVICE) $(FILE).elf

upload:
	avrdude -v -p $(DEVICE) -c $(PROGRAMMER) -P $(PORT) -b $(BAUD) -U flash:w:$(FILE).hex:i

clean:
	rm main.o
	rm main.elf
	rm main.hex