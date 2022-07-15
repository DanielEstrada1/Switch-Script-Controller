# Nintendo Switch Arduino Controller

Control your Nintendo Switch using a pro micro

Most of this readme is the same as [asottile's](https://github.com/asottile/switch-microcontroller) readme with a few changes.

## Requirements

- [pro micro] (or compatible) *Note you might want to find a version with the pins pre soldered if you are not able to solder them yourself
- [ftdi usb to uart] (or other uart device) *Pins need to be soldered for this one as well
- usb cables (both use [micro usb])
- wires (can use dupont wires or shorter jumper wires on a breadboard)
- breadboard to assemble everthing on

The following aren't necessary but useful depending on how you want to set up the arduino.
Each link is what I used for my setup
- [button] (for making flashing easier)
- [buzzer] (used for alerts like when the script finishes)
- [USB C to A Adapter] (used for connecting the pro micro to the switch in handheld mode)

[pro micro]: https://amzn.to/3rpb36r
[ftdi usb to uart]: https://amzn.to/3dRWML0
[micro usb]: https://amzn.to/2NVK4ll
[button]: https://a.co/d/ckQkAc4
[buzzer]: https://a.co/d/fZ3ZLA3
[USB C to A Adapter]: https://a.co/d/8hI48IK




## Installation

```
Working on Windows Instructions
```

## Assembly
For a video example of how to set up the board with dupont wires watch
[aosittle's video](https://youtu.be/chvgQUX7QaI) on youtube

The assembly is fairly straightforward, here is a rough diagram of the parts
and how they will be hooked up when operating

```
                        [your computer]
                            |
          +===========+     |
          | (ftdi)    |-----+ (usb cable)
          | gnd tx rx |
          +==-===-==-=+
             |   |  |
 +======+    |   |  |
 |buzzer|    |   |  |
 +======+    |   |  |  wires (note: tx matches with rx (crossed))
     |  |    |   |  |
    +-==-====-===-==-==+
    |9  gnd  gnd rx tx |-------------+  (usb cable)
    |     (pro micro)  |             |
    +==================+        [nintendo switch]

```

my assembly (I have a button from rst to gnd to help flashing)

![](https://user-images.githubusercontent.com/1810591/114293095-2ab8a980-9a48-11eb-9b35-290d58786701.jpg)

## Building

```bash
make MCU=atmega32u4
```

use the appropriate `MCU` for your board, the pro micro uses `atmega32u4`

## Flashing

you have to be quick with this!

- connect the pro micro to your computer
- short `rst` to `gnd` twice in quick succession

```bash
Working on Windows Instructions
```

Use the appropriate `MCU` and serial port for your board, the pro micro uses
`atmega32u4` and `/dev/ttyACM0`

## Usage

To use the controller:
- Start the game you want to play
- Connect the controller

After connecting the controller will be ready to receive inputs over serial.

Commands are sent over 9600 baud serial as single bytes and rebuilt on the arudino side.


I need to explain some behavior you will see when you connect the controller. Not every game displays the connecting of a controller the same. Some games such as Breath of the Wild and Celeste will display a prompt when connecting a new controller. Other games such as Pokemon will not display this screen. In most cases even without the prompt appearing the controller will be connected and ready to accept inputs over serial. If you have any issues you could always ensure you disconnect your controllers before plugging in the arduino and it'll work.

## Thanks

Thanks to Asottile for his [switch-microcontroller](https://github.com/asottile/switch-microcontroller) where I learned how to physically setup the project and how to communicate over serial with the pro micro

Thanks to Shiny Quagsire for his [Splatoon post printer](https://github.com/shinyquagsire23/Switch-Fightstick) and progmem for his [original discovery](https://github.com/progmem/Switch-Fightstick).

Thanks to bertrandom for his [snowball thrower](https://github.com/bertrandom/snowball-thrower) and modifications to the original project which helped me set up the start up script to connect the controller to the switch faster.
