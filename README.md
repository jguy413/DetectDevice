# DetectDevice
Device Detection Application with Physical LED Indicators


# Problem
While on a WFH Teams/Zoom/etc meeting, people (inlaws) are not always aware whether I am in a meeting. This has been at times awkward, because no matter the situation, one ends up thinking they looked like [this](https://www.youtube.com/watch?v=Mh4f9AYRCZY) in the background if they enter at a bad time! To avoid any embarrassment, I set out to provide those outside the home-office with an indication of the in-office meeting status. Additionally, this was also a great opportunity to get my feet wet with beginner circuitry/electronics.

# Overview
At a high-level, I quickly narrowed down the any solution to require 3 distinct components. The "software" running on the computer, the "hardware" or electrical circuit with an LED, and something to facilitate communication between these two.

# Software
Initially I thought I might give developing a Microsoft Teams application a try, as that is the video-chat app I use most often. However, the documentation + permissions issues eventually convinced me to seek other solutions. This ended up being a great thing, as I was able to come up with a much simpler solution that also scales to _any_ use of the camera. Modifying [code from @cobryan05](https://gist.github.com/cobryan05/8e191ae63976224a0129a8c8f376adc6) and digging into the Windows registry, I am able to track both the status of the microphone and the camera using Python.

In addition to the status of the physical devices, I also needed something to facilitate the communication between the Python code and the Arduino-compatible Elegoo Mega R3 2560 microprocessor; i.e., I was not prepared to translate the Python code into C and implement it into an Arduino sketch, so I needed outside help. I went with [pymata4](https://github.com/MrYsLab/pymata4), which works in tandem with the Firmata Express library uploaded to the board.

Finally, I run the .pyw script as a service via Windows Task Scheduler.

# Microprocessor
Main point here is that I opted for USB serial communication to provide information to the board, as opposed to a WiFi-based/other mechanism. I wanted to be able to understand as much of the system as possible, and the former felt like less of a rabbit-hole to fall into. In hindsight, I could have gotten away with a much simpler/smaller board given the few pins used in the end, so that may be a future modification so I can use the current microprocessor for something else.

# Hardware
I started by pursuing a circuit implementing a relay module. The idea being that a digitally-induced trigger would flip the relay from NO to NC and an independently-powered circuit would be "activated", resulting in a lit LED. Although I still like the idea for funzies, it seemed overcomplicated for "production" when I could just use the 5V provided by the microprocessor to power the LED. I was not going to delve into mains voltage on my first electronics project with the goal of someday having a second electronics project. Furthermore, a battery-powered circuit closed by the relay would just add to the number of physical components I needed to find a place for. So, relay-module eliminated.

My second thought was to use a serial-to-parallel converter. A big motivator here was just how fascinated I was by these pin-saving bad-boys when I read about them during the Elegoo tutorial. At this point I thought I would have 4 lights total -- two to indicate the camera is on, and two to indicate the microphone is in use (in a meeting). So, I would just need 2 of the 8 bits sent to the converter to trigger the LEDs for one light pair, and 2 different bits to trigger the LEDs for the other pair. However, after further consideration, I decided this was also an overcomplication. I was under no shortage of digital pins on the board, so why not just use a more direct approach?

Finally, I went with a super-simple implementation using only 2 LEDs! See the schematic below.

![image](https://user-images.githubusercontent.com/46940357/190284631-ba26d4ca-11aa-43fb-8356-c0a0400c49ec.png)

Although the final circuit used ended up being about as basic as it can get, I thoroughly enjoyed learning/experimenting with other methods. It's worth noting that even a simple circuit like this still takes time to implement when soldering wires for the first time...

# Result

Microprocessor connected with Firmata Express sketch uploaded.

![image](https://user-images.githubusercontent.com/46940357/190286520-16833338-4204-4823-b9e5-da6f2f7d4b7b.png)


Solder/Heatshrink: Soldered GND wires from parallel circuits to reduce wires used.

![image](https://user-images.githubusercontent.com/46940357/190286665-e0feff2d-46eb-4b62-a32e-ee5717012448.png)


Not in a meeting, safe to enter!

![image](https://user-images.githubusercontent.com/46940357/190286731-7c198fa7-d819-4aed-ab01-b32720867ca5.png)


In a meeting, but the camera isn't on -- enter at your own risk!

![image](https://user-images.githubusercontent.com/46940357/190286798-7d543d46-3d5b-4343-b93d-32cba6ee5047.png)


In a meeting, and the camera is on -- don't come in!

![image](https://user-images.githubusercontent.com/46940357/190286842-8b8722e1-fd51-453a-a2b9-2431c7fb0d6a.png)



