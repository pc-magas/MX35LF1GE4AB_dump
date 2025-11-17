import spidev

# Create SPI object
spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, device 0
spi.max_speed_hz = 50000

device_id=0xC212

# Send and receive data
resp = spi.xfer2([0x09])
print(resp)
if(resp == device_id):
    print("Macronix MX35LF1GE4AB found")
    print("Device Id:"+resp) 
else:
    print("Device not found")
    exit(1)

spi.close()