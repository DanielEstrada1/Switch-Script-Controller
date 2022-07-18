# Nintendo Switch Arduino Controller

Control your Nintendo Switch using a pro micro

# Differences to asottile's switch microcontroller
Sections of this readme is the same as [asottile's](https://github.com/asottile/switch-microcontroller) readme with some changes.

Asottile's project sends commands as single-byte ascii characters and executes them as they are received. While this method works it would require the user to create a case for every set of instructions you would want.

I have changed the code to use two bytes to build more complex instructions. This allows us to remove the need to use individual cases for every command. Now using the two bytes together we can update our buttons, sticks, or dpad. 

This update works by checking sets of 2 bits to determine what kind of data the controller has received and update our commands appropriately.

The way each command is structured is like so
```
 |--- The first two bits are always used to determine how to use the remaining 14 bits
 V
|00|00 0000 0000 0000| = Buttons
    ^---These 14 bits represent each button
|00|00 0000|0000 0000| = Left/Right Stick X/Y values
        ^      ^--- Since each stick can only be 0-255 we only use two bytes or the last 8 bits
        |---We use bits 8 and 9 to tell us if we are LX,LY,RX,or RY values
|00|00 0000 0000|0000| = Dpad Direction
    ^             ^---Dpad is represented with only one byte or the last 4 bits
    |---We do not use these 10 bits
```
This method allows us to build more complex instruction without needing to make cases for each input we want and send less data through the serial. This is all handled within Joystick.c where I have included comments to explain what my code does.


If you want to execute a Shield Surf in Breath of the Wild the script will look like this
```
2,16460,33024,0.2
```
The first number 2 is used to tell the arduino that it is receiving two inputs
16460 in binary is
```
0100 0000 0100 1100
```
The first two bits 01 tell the arduino we are pressing buttons
the following 14 bits represent each button
from left to right we have Capture, Home, Right Click, Left Click, +, -, ZR, ZL, R, L, X, A, B,Y
```
00 0000 0100 1100
```
these 14 bits tell us that we are pressing the A,X, and ZL buttons
The next number 33024 is broken in a similar pattern
```
1000 0001 0000 0000
```
This time the first two bits 10 tell us we are updating a stick value
since sticks only need two bytes our number is broken up into 
```
10 000001 00000000
```
where using bits 8 and 9 tells us we are a left stick Y value
and the final 2 bytes 0000 0000 tell us to update our Y value from neutral to 0

the very last number 0.2 is a duration that our program will wait before sending the next instruction to the arduino

I have also created a GUI using PyQt to allow for an easier time creating, editing, and testing scripts. You can also use the included python script to run each script from command line without the need of using the gui.


## Requirements

- [pro micro] (or compatible) *Note you might want to find a version with the pins pre soldered if you are not able to solder them yourself
- [ftdi usb to uart] (or other uart device) *Pins need to be soldered for this one as well
- usb cables (both use [micro usb])
- wires (can use dupont wires or shorter jumper wires on a breadboard) I used [these](https://a.co/d/g2ouoll) and [these](https://a.co/d/6faDum1) but you only need one. I'd recommend the shorter jumper cables for the breadboard to keep things clean
- breadboard to assemble everthing on. I used [these](https://a.co/d/7jASLaS)

The following aren't necessary but useful depending on how you want to set up the arduino.
Each link is what I used for my setup
- [button] (for making flashing easier)
- [buzzer] (used for alerts like when the script finishes however at the moment there is no code to activate it)
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
Since I use Windows the following instructions are for Windows users and show how I got the project working.
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
    
    Download Avrdude for Windows from this [github](https://github.com/mariusgreuel/avrdude/releases) as well as the AVR 8-Bit Toolchain (Windows) from Atmel's website [here](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio/gcc-compilers).
    After unzipping both of these files we will then move them to the C:\Program Files folder. Make sure that you move the folder within the avr8-gnu-toolchain-3.7.... folder you downloaded from Atmel. I took the time to rename this long file to avr8-gnu-toolchain.
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
6. Optional Steps
    At this point you can move on if you are planning to only use the included scriptGUI.exe. If you are planning to use the python version of the gui, or the python file to run scripts from the command line then you will need to
    1. Install [python](https://www.python.org/downloads/) 
    2. Install PyQt (Use this after install python)
        ```
        pip install pyqt6
        ```
    3. Install pyserial
        ```
        pip install pyserial
        or
        python -m pip install pyserial
        ```
    After installing these you can run the python file for the gui with
    ```
    python3 -m scriptGui
    ```
    The included runScript.py will run a script of your choice from the commandline
    ```
    python3 -m runScript --file x --port x --count x 
    ```
    File is the name of the specific file you want to run.
    
    Port is what port to connect to.
    
    Count is how many times you want to repeat the script

# Building
Finally after all that work we can build our project. Open up a terminal in our project folder and run this command.
Make sure to use the proper `MCU` for your board. The pro micro we are using uses `atmega32u4`
```
make MCU = atmega32u4
```

# Flashing

When flashing the arduino make sure to use the correct `MCU` and serial port for your board. The pro micro uses `atmega32u4` for the `MCU`. When using a Windows machine we use the `COM` port
You'll have to figure out what port your pro micro is connected to on your computer.
The easiest way to do this is to search for device manager in your windows search bar and open it.

![Screenshot 2022-07-17 213916](https://user-images.githubusercontent.com/36652048/179446230-57334197-8ce9-4449-8c02-19e37d005cb6.JPG)

Then head down to Ports(COM & LPT) and plug in your arduino to your computer. You should see the arduino boot loader as well as what COM it is connected too as shown here.

![Screenshot 2022-07-17 214048](https://user-images.githubusercontent.com/36652048/179446456-e296cb35-9803-4755-9785-1bcab3392dbb.JPG)

For me the port I need to specify to flash the Arduino is `COM8`

If the bootloader is not showing up you will ahve to short `rst` and `gnd` to reset the arduino into it's bootloader.

In order to flash our arduino with our program you will have to perform the following steps quickly
- connect the pro micro to your computer
- short `rst` to `gnd` twice in quick succession
- then hit enter with this command in your terminal (the terminal should be opened to our project folder)
```
avrdude -v -cavr109 -patmega32u4 -PCOM_ -b57600 -D -Uflash:w:Joystick.hex:i
```

Replace the _ in -PCOM_ with the correct COM number we found previously using the Device Manager.


## Usage
Commands are sent over 9600 baud serial as a series of bytes and rebuilt on the arudino side.
To be able to send data to the Arduino we will have to find the correct port for our ftdi controller. You can find this port the same way we found the Arduino Bootloader port by plugging in our FTDI controller to our pc and checking the device manager again.

![Screenshot 2022-07-18 142157](https://user-images.githubusercontent.com/36652048/179619705-ed322178-7ccc-4aa2-9122-8b9811abd8bc.JPG)

For me this would be `COM7` but could be different for you.

Make sure you turn on Pro Controller Wired Communication in your System Settings under Controllers and Sensors so the Switch will allow the Arduino to connect.

<img width="700" src ="https://user-images.githubusercontent.com/36652048/179632920-fabf20f6-52d9-406e-ad0e-2c665624f480.JPG">


To use the controller:
- Start the game you want to play
- Connect the controller

After connecting to the switch the controller will be ready to receive input

When connecting the arduino to the switch you may or may not see a connecting screen. Games such as Breath of The Wild and Celeste display the connecting screen while some games like Pokemon do not. In most cases you will be able to start sending commands but in the event it is not responding then make sure you disconnect your controllers before plugging in the arduino.

![test](https://user-images.githubusercontent.com/36652048/179449842-f3eeb687-27a0-49c0-aee9-dd8f612277a0.gif)

Before you start to make your own scripts it is important to understand how the Arduino is working. When the arduino receives a new instruction it will update itself according to the data received. If it receives the signal to press the A button it will press the A button. It will continue to hold the A button until it receives a new instruction where it will update itself accordingly. This is equivalent to saying that to register an A button press you have to send one instruction to hold the button and a second instruction to release the button.

Included in this project is a Gui I created to make it easier to make scripts to send to the arduino. I have also included a python file that will send your created scripts to the arduino without the need of opening the gui everytime you wish to use the arduino

![Screenshot 2022-07-18 141321](https://user-images.githubusercontent.com/36652048/179618577-2a3a1a57-5b0f-46ed-ae62-f3dce279b1e7.JPG)

The left side of the Gui is used to select what buttons you want to press, how far to push the right/left stick, what dpad direction to press, as well as how long you want these buttons to be pressed. You can also include a comment with each instruction.

1. Face Buttons
    - There are 14 buttons to represent each button on a Switch Controller and can be toggled on and off
2. Left/Right Stick X/Y Values
    - When inputting a value for the sticks there are some things to remember about their orientation and values
    - You can input any whole number between 0 and 255
    - Inputting a 0 for the X Value will push the stick left, 128 will represent neurtral and is the default, and 255 will push the stick to the right.
    - Inputting a 0 for the Y Value will push the stick up, 128 will represent neutral and is the default, and 255 will push the stick down.
    - Any value in between those 3 numbers can be used to generate more delicate stick movements. For example walking instead of running when games auto run if you push the stick all the way in one direction
    - You can submit X/Y for both Left/Right Sticks when making a new instruction for the Arduino
3. Dpad
    - The Dpad however is unique that you can only push one direction per command. Selecting more than one will deselect the last input pressed as the Dpad can only be one direction per instruction
4. Input Duration
    - The input duration will represent in seconds how long you want an instruction to be executed.
    - This input does support decimals up to 2 places so something like .01 is valid however I have not tested if games will respond properly at that time. I usually only use .1 for quick presses of buttons
5. Comment
    - You can input a comment to help you keep track of what is occuring at each step of your script. Since all these scripts are made of multiple button presses it helps to keep comments to remember what action is happening at what point in the script
6. Clear
    - Pressing the clear button will clear all the buttons,stick values,dpad button, duration, and comments currently inputted
7. Submit
    - Pressing the submit button will add it to the first list of the gui.
    - Clicking on an entry in the list will let you drag them around to rearrange them.
    - If an entry in the list is selected pressing submit will add your new instruction above the currently selected one
    - Right Clicking on the entry will allow you to edit or delete the entry
    - When editing a value pressing submit will update the entry you had selected to edit. Clicking another value will make it so the submit button will add the new instruction to the list instead of updating the one that was originally selected to be edited
8. Serial Port
    - Here you can input which Port is connected to your FTDI controller so you can send the currenlty loaded script
    - If there is an error the list on the right side of the GUI will update with the error message
9. Count
    - This entry is used to input how many times you want the arduino to run the same script
    - The default is one if there is no entry
10. Run Script
    - Pressing this button will attempt to send the currently loaded instructions to the arduino.
    - Errors will be shown in the list on the right side of the GUI
11. Stop Script
    - Pressing this button will stop running the current script and send an instruction to the arduino to reset itself to netural where no input is pressed

Here is an example of a simple Shield Surf Script for Breath of The Wild

![Screenshot 2022-07-18 144954](https://user-images.githubusercontent.com/36652048/179623485-cbd6f6b5-9bcb-4b98-84fd-683bb25b2772.JPG)

After hitting run script the gui will update as it sends each command and look like this at the end
![Screenshot 2022-07-18 144240](https://user-images.githubusercontent.com/36652048/179622604-5b7dfc9d-f6d5-4f7f-8e00-1bbe09dbaad0.JPG)

While the script runs you should see this on your Switch
![test](https://user-images.githubusercontent.com/36652048/179623865-9da0695e-8906-4cf4-91ea-34faf5d50ec7.gif)


## Thanks

Thanks to Asottile for his [switch-microcontroller](https://github.com/asottile/switch-microcontroller) where I learned how to physically setup the project and how to communicate over serial with the pro micro

Thanks to Shiny Quagsire for his [Splatoon post printer](https://github.com/shinyquagsire23/Switch-Fightstick) and progmem for his [original discovery](https://github.com/progmem/Switch-Fightstick).

Thanks to bertrandom for his [snowball thrower](https://github.com/bertrandom/snowball-thrower) and modifications to the original project which helped me set up the start up script to connect the controller to the switch faster and for adding lufa as a submodule and including the git command as well.
