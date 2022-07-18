# Nintendo Switch Arduino Controller

Control your Nintendo Switch using a pro micro

# Differences to asottile's switch microcontroller
Sections of this readme is the same as [asottile's](https://github.com/asottile/switch-microcontroller) readme with some changes.

Asottile's project sends commands as single-byte ascii characters and executes them as they are received. While this method works it would require the user to create a case for every set of instructions you would want.

I have changed the code to use two bytes to build more complex instructions. This allows us to remove the need to use individual cases for every command. Now using the two bytes together we can update our buttons, sticks, or dpad. 

This update works by checking sets of 2 bits to determine what kind of data the controller has received and update our commands appropriately.

I have also created a GUI using PyQt to allow for an easier time creating, editing, and testing scripts. You can also use the included python script to run each script from command line without the need of using the gui.


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

## Assembly
For a video example of how to set up the board with dupont wires watch
[aosittle's video](https://youtu.be/chvgQUX7QaI) on youtube

Aosittle's diagram is pretty straightforward and easy to follow

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

This is how I set up my board.

<img width="700" src ="https://user-images.githubusercontent.com/36652048/179428633-f0b2ff2f-2479-4bb1-96b6-76d6af0e2d2e.jpg">


## Installation and Compiling the project
Since I use windows the following instructions are for windows users and show how I got the project working.
What you will need
- Git
- Avrdude
- GNU Make
- The latest Atmel GNU toolchain

You will only need to install Python/PyQt if you want to run the GUI from the python file or scripts using the included python file without using the GUI
- Python3 [Download](https://www.python.org/downloads/)
- Latest version of PyQt (used for the GUI) (Can be installed after installing python using pip)

1. Install Git
    Follow the git installation instructions [here](https://github.com/git-guides/install-git).
    After installing git you can clone the repository with this command to include the LUFA submodule
    ```
    git clone --recursive https://github.com/DanielEstrada1/Switch-Script-Controller.git
    ```
2. Install Chocolatey package manager
    There are various ways to get the make command to work on windows but I found Chocolatey to be the easiest. Follow their instructions to install chocolatey onto your windows machine [here](https://chocolatey.org/install).
    After installation use this command from an administrative shell to install make onto your windows machine.
    ```
    choco install make
    ```
3. Download Avrdude and Atemel GNU toolchain
    Download Avrdude for windows from this [github](https://github.com/mariusgreuel/avrdude/releases) as well as the AVR 8-Bit Toolchain (Windows) from Atmel's website [here](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio/gcc-compilers).
    After unzipping both of these files we will then move them to the C:\Program Files folder. Make sure that you move the folder within the avr8-gnu-toolchain folder you downloaded from Atmel.
4. Updating Environment Variables to include paths to AVRDUDE and Atmel tool chain
    After moving the files you'll want to head over to your system environment variables and edit your user variable PATH to include the bin folder from the avr8-gnu-toolchain as well as the avrdude folder as shown here

<img width="500" src ="https://user-images.githubusercontent.com/36652048/179445047-1f37245e-71d3-4ce1-83f8-e11398386c5c.png">

5. Testing our work
    From here we can do a quick test from git bash or your terminal of choice by running these lines
    ```
    avr-gcc --version
    make -v
    ```
    you should see something like this
    
    ![246996910 96_image](https://user-images.githubusercontent.com/36652048/179445726-e025de01-df28-4d2a-96ca-bb85abb33c6c.png)

# Building
Finally after all that work we can build our project. Open up a terminal in our project folder and run this command.
Make sure to use the proper `MCU` for your board. The pro micro we are using uses `atmega32u4`
```
make MCU = atmega32u4
```

# Flashing

Use the appropriate `MCU` and serial port for your board, the pro micro uses
`atmega32u4` and `COM`. You'll have to figure out what port your pro micro is connected to on your computer.
The easiest way to do this is to search for device manager in your windows search bar and open it.

![Screenshot 2022-07-17 213916](https://user-images.githubusercontent.com/36652048/179446230-57334197-8ce9-4449-8c02-19e37d005cb6.JPG)

Then head down to Ports(COM & LPT) and plug in your arduino to your computer. You should see the arduino boot loader as well as what COM it is connected too as shown here.

![Screenshot 2022-07-17 214048](https://user-images.githubusercontent.com/36652048/179446456-e296cb35-9803-4755-9785-1bcab3392dbb.JPG)

If the bootloader is not showing up you will ahve to short `rst` and `gnd` to reset the arduino into it's bootloader.
In order to flash our arduino with our program you will have to perform the following steps quickly
- connect the pro micro to your computer
- short `rst` to `gnd` twice in quick succession
- then hit enter with this command in your terminal
```
avrdude -v -cavr109 -patmega32u4 -PCOM_ -b57600 -D -Uflash:w:Joystick.hex:i
```

Replace the _ in -PCOM_ with the correct COM number we found previously using the Device Manager.


## Usage
Commands are sent over 9600 baud serial as a series of bytes and rebuilt on the arudino side.
To use the controller:
- Start the game you want to play
- Connect the controller

After connecting to the switch the controller will be ready to receive input

When connecting the arduino to the switch you may or may not see a connecting screen. Games such as Breath of The Wild and Celeste display the connecting screen while Pokemon does not. In most cases you will be able to start sending commands but in the event it is not responding then make sure you disconnect your controllers before plugging in the arduino.

![test](https://user-images.githubusercontent.com/36652048/179449842-f3eeb687-27a0-49c0-aee9-dd8f612277a0.gif)

Included in this project is a Gui I created to make it easier to make scripts to send to the arduino

## Thanks

Thanks to Asottile for his [switch-microcontroller](https://github.com/asottile/switch-microcontroller) where I learned how to physically setup the project and how to communicate over serial with the pro micro

Thanks to Shiny Quagsire for his [Splatoon post printer](https://github.com/shinyquagsire23/Switch-Fightstick) and progmem for his [original discovery](https://github.com/progmem/Switch-Fightstick).

Thanks to bertrandom for his [snowball thrower](https://github.com/bertrandom/snowball-thrower) and modifications to the original project which helped me set up the start up script to connect the controller to the switch faster and for adding lufa as a submodule and including the git command as well.
