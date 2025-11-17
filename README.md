# MX35LF1GE4AB_dump

Dump Macronix MX35LF1GE4AB flash memory chip

## Install upon raspberry pi

### Step 1 install dependencies

```
git clone git@github.com:pc-magas/MX35LF1GE4AB_dump.git
cd ./MX35LF1GE4AB_dump
sudo apt-get install python3-spidev
```

### Step 2 Config SPI

Follow instructions upon: https://www.raspberrypi.com/documentation/computers/configuration.html

## PIN configuration

| Flash Memory | Raspberry Pi | GPIO pin |
|-----------|--------|---------|
| CS        | Pin 24 | GPIO 8 (SPI CE0)  |
| SI/SIO0   | Pin 19 | GPIO 10 (SPI0 MOSI) |
| SO/SIO1   | Pin 21 | GPIO 9  (SPI0 MISO)|
| WP#/SIO2  | One of PINS 9,6,25,30,30,39 | GROUND |
| SCLK      | Pin 23 | GPIO 11 (SPI0 SCLK) |
| HOLD#/SIO3| Either PIN 1 or pin 17 | 3.3V |
| VCC       | Either PIN 1 or pin 17  | 3.3V |
| GND       | One of PINS 9,6,25,30,30,39 | GROUND |

## SPI device
The spidevice is the 0,0