# Hand Command
Taking notes and your keyboard is too far away? You can now control your screen when you're too far away from the keyboard! 

This project uses your camera and computer vision to create keyboard controls (aka for people like me who are too lazy to touch their keyboard to control their screens). 

Any suggestions are welcome!


## Installation
Hand Command uses python and utilizes opencv, tkinter, and google's mediapipe ML to detect hand recognition. Apart from the standard python modules, you would also need to install mediapipe and opencv:

Mediapipe: pip install mediapipe

Opencv: pip install opencv-contrib-python

This project has been tested using python 3.9.5 on windows.

## QuickStart
Run 'python HandTrack.py' and put your hand in a place where the camera can see and the program should automatically be in mouse mode. 

Note: You can uncomment line 158 in HandTrack.py to see what your camera is seeing.

## Guide
There are four modes currently implemented: mouse mode, switching window mode, switching tab mode, and music mode

Finger command recognition is determined by whether a given finger is straight and pointing outwards or not. Note that it is better to have the face of your palm facing the camera. 

The commands below describe which fingers should be straight and out, all other fingers should be curled/closed. e.g. A command of 'Thumb' means a closed fist with your thumb sticking out. A command of 'Index and Middle' means your index and middle finger are pointing straight up while your other fingers are curled.

General Commands (included in all modes):
```
Closed Fist - Do nothing

Ring - Quit running the program

Index, Middle, Ring, and Pinky  - Show settings window

Open hand (all fingers out) - Switch modes
```

Settings Window
```
The four modes will show up on a new window.You have to manually 
(use the mouse) change the settings as they wish.Finally, close the 
window to exit the settings.

Keeping a mode checked will keep that mode active when you switch modes,
 keeping a mode unchecked means that mode will never be switched to. 
 For example, if we only want the music mode, we can uncheck everything 
 but music mode (meaning switching modes will do nothing). Note that if 
 everything is unchecked, then mouse mode will be on by default
```

Mouse Mode
```
Index and Middle - Hold both of these fingers up and move them around to control your mouse (note the mouse movement is dependent solely on your middle finger).

Index and Middle + Thumb - Left Click

Index and Middle + Pinky - Right Click
```

Switch Window Mode
```
Index and Middle - AltTab (but only once)

Index, Middle, and Ring - WinTab

Index - Presses Enter key

Thumb - Presses Left Arrow key

Pinky - Presses Right Arrow key
```

Switch Tab Mode
```
Thumb - Presses Ctrl + Shift + Tab

Pinky - Presses Shift + Tab

Index and Middle - Scroll down

Index, Middle, and Ring - Scroll up
```

Music Mode
```
Thumb - Increases volume

Pinky - Decreases volume

Index - Mute/Unmute

Index and Middle - Play/Pause
```