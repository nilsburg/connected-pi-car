# Connected PI-CAR

This project aims to develop a device to track your car.

### Hardware
- [Raspberry PI Zero WH](https://www.raspberrypi.org/blog/zero-wh/). The same as the Raspberry PI Zero W but with headers.
- Waveshare [SIM7000E NB-IoT HAT](https://www.waveshare.com/SIM7000E-NB-IoT-HAT.htm)
- ODB2 device (TODO)

### Setup
At this moment I only have the SIM700E HAT and it is possible to use it without the Raspberry Pi just connecting it through USB to your PC. Detailed instructions on how to make it work on Windows are [here](https://www.waveshare.com/wiki/File:SIM7000E-NB-IoT-HAT-Manual-EN.pdf).

There are two scripts (Python3):
- device.py (this one is supposed to run in the raspberry pi)
- client.py (this one sends the request to obtain the position)

The communication is done using MQTT. For this example I am using [HiveMQ](https://www.hivemq.com) a free MQTT broker to do the tests. But you can easily install a broker on your own server.

You can edit __device.py__ if you want to change the COM PORT (default 25 and baudrate 9600) on which the SIM7000E is connected and the MQTT config.

Still lot of work to do!