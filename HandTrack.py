import cv2
import mediapipe as mp
import time
from KeyboardControl import keyboardControl
from PositionDetect import positionDetector

class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionConf = 0.7, trackConf = 0.7):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, maxHands, detectionConf, trackConf)
        self.mpDraw = mp.solutions.drawing_utils
    
    # Use mediapipe to find hands
    def findHands(self, img, draw = False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0, draw = False):
        landmarks = []
        if not self.results.multi_hand_landmarks:
            return []
        
        if len(self.results.multi_hand_landmarks) > handNo and handNo >= 0:
            hand = self.results.multi_hand_landmarks[handNo]
            h, w, c = img.shape
            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)
        return landmarks

class settings():
    def __init__(self):  
        self.cooldownTime = 0.5
        self.keyboard = keyboardControl()
        self.modes = ['mouse mode', 'switch tab mode', 'music mode']
        self.activeModes = self.modes
        self.index = 0
        self.lastOperation = 'reset'
        self.reset()
    
    def incIndex(self):
        self.index = (self.index + 1) % len(self.modes)

    def reset(self):
        self.positions = ['reset', 'handClosed', 'handOpen', 'indexMiddle', 'indexMiddleRing', 'thumbIndexMiddle', 
        'pinkyIndexMiddle', 'thumb', 'index', 'ring', 'pinky']
        self.setMode()
        self.lastCalled = {}
        for i in self.positions:
            self.lastCalled[i] = 0
    
    def setMode(self):
        if self.index == 0:
            self.mouseMode()
        elif self.index == 1:
            self.switchTabMode()
        elif self.index == 2:
            self.musicMode()
        self.fillEmptyPos()
    
    def fillEmptyPos(self):
        for i in self.positions:
            if not i in self.settings:
                self.settings.update({i: [self.keyboard.nothing, 1]})
        self.settings.update({'ring': [exit, 4]})
        self.settings.update({'handOpen': [self.modeSwitch, 1]})
    
    # Sets to mouse mode with the corresponding hand positions and functions called
    def mouseMode(self):
        self.settings = {
            'indexMiddle': [self.keyboard.moveMouse, 1],
            'thumbIndexMiddle': [self.keyboard.click, 0.5], 
            'pinkyIndexMiddle': [self.keyboard.rightClick, 0.5]}
    
    # Sets to tab switching mode with the corresponding hand positions and functions called
    def switchTabMode(self):
        self.settings = { 
            'indexMiddle': [self.keyboard.altTab, 2],
            'indexMiddleRing': [self.keyboard.winTab, 2],
            'index': [self.keyboard.enter, 1],
            'thumb': [self.keyboard.leftArrow, 1],
            'pinky': [self.keyboard.rightArrow, 1]}
    
    def musicMode(self):
        self.settings = {
            'thumb': [self.keyboard.volumeup, 0.05],
            'pinky': [self.keyboard.volumedown, 0.05],
            'index': [self.keyboard.volumeMute, 1]
        }

    def modeSwitch(self):
        self.incIndex()
        self.keyboard.alert(self.activeModes[self.index])
        self.setMode()
    
    def operate(self, key, optionalBool = True):
        if time.time() - self.lastCalled[key] > self.cooldownTime * self.settings[key][1] and optionalBool:
            self.settings[key][0]()
            self.lastCalled[key] = time.time()
            self.lastOperation = key

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    pos = positionDetector()
    s = settings()

    startTime = time.time()
    while True:
        if time.time() - startTime > 120:
            break
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = detector.findHands(img, True)
        lmList = detector.findPosition(img)

        if len(lmList) == 0:
            lastCooldownTrigger = time.time()
            continue
        pos.update(lmList)
        
        # Everything that needs cooldown
        if pos.isHandOpen():
            s.operate('handOpen', s.lastCalled['handClosed'] >= s.lastCalled['handOpen'])
        elif s.activeModes[s.index] == 'mouse mode' and (pos.areFingersStraight([1,2]) or pos.areFingersStraight([0,1,2]) or pos.areFingersStraight([1,2,4])):
            newPos = [lmList[12][1], lmList[12][2]]
            firstCall = time.time() - s.lastCalled['indexMiddle'] > s.cooldownTime / 2
            # Thumb is out, so left click
            s.operate('thumbIndexMiddle', pos.isFinger(0))
            # Pinky is out, so right click
            s.operate('pinkyIndexMiddle', pos.isFinger(4))
            s.settings['indexMiddle'][0](firstCall, newPos)
            s.lastCalled['indexMiddle'] = time.time()
        elif pos.areFingersStraight([1,2]):
            s.operate('indexMiddle')
        elif pos.areFingersStraight([1,2,3]):
            s.operate('indexMiddleRing')
        elif pos.areFingersStraight([0]):
            s.operate('thumb')
        elif pos.areFingersStraight([1]):
            s.operate('index')
        elif pos.areFingersStraight([3]):
            s.operate('ring', s.lastOperation == 'ring', 4)
        elif pos.areFingersStraight([4]):
            s.operate('pinky')
        elif pos.areFingersStraight([]):
            s.operate('handClosed')
        else:
            s.lastCalled['reset'] = time.time()
            print("nothing")

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()