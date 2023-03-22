CFLAGS ?= -Os -DF_APU=16000000UL -mmcu=atmega328p
LDFLAGS ?= -mmcu=atmega328p
# Path where your Arduino Uno is connected to
ARDUINO_USB ?= /dev/ttyACM0

all: stepper.hex

stepper.hex: stepper
	avr-objcopy -O ihex -R .eeprom stepper stepper.hex

stepper: stepper.o
	avr-gcc $(LDFLAGS) -o $@ $^

stepper.o: stepper.c
	avr-gcc $(CFLAGS) -c -o $@ $<

deploy: stepper.hex
	avrdude -F -V -c arduino -p ATMEGA328p -P ${ARDUINO_USB} -b 115200 -U flash:w:stepper.hex  

clean: FRC
	rm -f stepper.elf stepper.hex stepper.o stepper

FRC: