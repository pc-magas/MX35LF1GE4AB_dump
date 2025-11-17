import spidev

# Create SPI object
spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, device 0
spi.max_speed_hz = 50000

# Send and receive data
resp = spi.xfer2([0x9F, 0x00, 0x00, 0x00])
print(resp)
if(resp[2] == 0xC2):
    print("Macronix MX35LF1GE4AB found")
    if(resp[3] == 0x12):
	    print("Device type is SERIAL NAND flash chip")
    else:
	    print("Uknown type")
	    exit(1)
else:
    print("Device not found")
    exit(1)

print("Get features")

resp = spi.xfer2([0x0F, 0xB0, 0x00, 0x00])

print(resp)

spi.close()
