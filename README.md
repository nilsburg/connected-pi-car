# Connected PI-CAR

This project aims to develop a device to track your car.

### Hardware
- [Raspberry PI Zero WH](https://www.raspberrypi.org/blog/zero-wh/). The same as the Raspberry PI Zero W but with headers.
- Waveshare [SIM7000E NB-IoT HAT](https://www.waveshare.com/SIM7000E-NB-IoT-HAT.htm)
- ODB2 device
- M2M SIM Card [Things Mobile](https://www.thingsmobile.com/private/thingsmobile)
- microsd card for the raspeberry pi

### Software
- Raspbian buster
- python3

### Setup
The first steps are to enable the rpi to access the serial port.
First edit the file __/boot/config.txt__ and add
```
enable_uart=1
```
Then we need to disable the Linux's use of console UART:
```
sudo raspi-config
```
Select option 5, __Inerfacing options__, then P6,__Serial__ and select __No__. Then exit raspi-config
Then reboot.

After this you should be able to communicate to the serial port, in my case it is __/dev/ttyS0__ and baudrate 9600.  
[minicom](https://help.ubuntu.com/community/Minicom) is a great tool to communicate to the serial port:
```
sudo minicom -D /dev/ttyS0 -b 9600
```
Then you can start launching AT commands:
```
AT+CGMM //checks the module name
```
(to exit minicom press Ctrl+A and the select exit)

### TODO
- Upload python samples
- Write more documentation
- Add instructions to enable SIM card

### Reference:
- https://www.raspberrypi.org/documentation/configuration/uart.md
- https://www.waveshare.com/wiki/SIM7000E_NB-IoT_HAT
