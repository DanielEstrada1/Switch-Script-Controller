from __future__ import annotations

import argparse
import sys
import time

import serial

SERIAL_DEFAULT = 'COM1' if sys.platform == 'win32' else '/dev/ttyUSB0'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default="script.txt")
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--serial', default=SERIAL_DEFAULT)
    args = parser.parse_args()
    
    with serial.Serial(args.serial, 9600) as ser:
        try:
            with open(args.file, 'r') as f:
                lines = f.readlines()
                instructions = []
                for line in lines:
                    line = line.strip()
                    firstSplit = line.split(",",1)
                    num = int(firstSplit[0])
                    restOfString = firstSplit[1].split(',',num + 1)
                    restOfString.pop()
                    instructions.append(num)
                    instructions.extend(restOfString)
                for _ in range(args.count):
                    print(instructions)
                    print("Count: " +  str(_))
                    loc = 0
                    while loc < len(instructions):
                        instructCount = int(instructions[loc])
                        loc += 1
                        if instructCount != 0:
                            ser.write(instructCount.to_bytes(1, 'little'))
                            ser.read()
                            for x in range(instructCount):
                                temp = int(instructions[loc])
                                ser.write((temp & 0xff).to_bytes(1, 'little'))
                                ser.read()
                                ser.write(((temp>>8) & 0xff).to_bytes(1, 'little'))
                                ser.read()
                                loc += 1
                        else:
                            ser.write((1).to_bytes(1, 'little'))
                            ser.read()
                            ser.write((0).to_bytes(1, 'little'))
                            ser.read()
                            ser.write((0).to_bytes(1, 'little'))
                            ser.read()
                        time.sleep(float(instructions[loc]))
                        loc += 1
        except IOError as e:
            print("Could not open file: " + args.file)
        ser.write((1).to_bytes(1, 'little'))
        ser.read()
        ser.write((0).to_bytes(1, 'little'))
        ser.read()
        ser.write((0).to_bytes(1, 'little'))
        ser.read()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
