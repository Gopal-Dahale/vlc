# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import matplotlib.pyplot as plt

# Software SPI configuration:
CLK = 18
MISO = 23
MOSI = 24
CS = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

print('Reading MCP3008 values, press Ctrl-C to quit...')

# Read all the ADC channel 0 values in a list.
values = []
channel = 0
count = 50
# Main program loop.
for _ in range(count):
    # The read_adc function will get the value of the specified channel (0-7).
    x = mcp.read_adc(channel)
    values.append(x)
    # Print the ADC values.
    print('Channel %d: %d' % (channel, x))
    # Pause for half a second.
    time.sleep(0.5)

plt.plot(values)
plt.xlabel('time')
plt.ylabel('ADC output')
plt.title('Plot to distinguish 0s and 1s')
plt.show()
