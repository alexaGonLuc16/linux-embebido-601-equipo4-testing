PRG = secuencia
SOURCE = secuencia.c

MCU = atmega328p

CC = aver-gcc

CFLAGS		 = -g -Wall -OSs -mmscu=$(MCU)

OBJCOPY		 = avr-objcopy
OBJDUMP 	 = avr-objdump

all: ofile text

clean:
	rm -rf *.o $(PRG)
	rm -rf *.hex

ofile:
	$(CC) $(SOURCE) -o $(PRG) -Wall -Os -mmcu=$(MCU) -l.

text: hex

hex: $(PRG).hex

%.hex:
	$(OBJCOPY) -O ihex $(PRG) $(PRG).hex
install: clean all
	sudo avrdude -p $(MCU) -c usbtiny -v -U flash:w:$(PRG).hex:i
