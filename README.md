# nintendo switch controller arduino

control your Nintendo Switch using a pro micro

## requirements

- [pro micro] (or compatible)
- [ftdi usb to uart] (or other uart device)
- usb cables (both use [micro usb])
- wires

[pro micro]: https://amzn.to/3rpb36r
[ftdi usb to uart]: https://amzn.to/3dRWML0
[micro usb]: https://amzn.to/2NVK4ll

## installation

```
Working on Windows Instructions
```

## assembly

the assembly is fairly straightforward, here is a rough diagram of the parts
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

## building

```bash
make MCU=atmega32u4
```

use the appropriate `MCU` for your board, the pro micro uses `atmega32u4`

## flashing

you have to be quick with this!

- connect the pro micro to your computer
- short `rst` to `gnd` twice in quick succession

```bash
sudo avrdude -v -patmega32u4 -cavr109 -P/dev/ttyACM0 -Uflash:w:output.hex
```

use the appropriate `MCU` and serial port for your board, the pro micro uses
`atmega32u4` and `/dev/ttyACM0`

## Usage

to use the controller:
- start the game you want to play
- press home
- navigate to controllers
- change order/grip
- at this point, connect the controller (it should register itself and start
  the game)

at this point, you can control the controller using uart

## thanks

Thanks to Shiny Quagsire for his [Splatoon post printer](https://github.com/shinyquagsire23/Switch-Fightstick) and progmem for his [original discovery](https://github.com/progmem/Switch-Fightstick).
Also thanks to bertrandom for his [snowball thrower](https://github.com/bertrandom/snowball-thrower) and all the modifications.
