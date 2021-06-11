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
        self.reset()
        self.modes = ['mouse mode', 'switch tab mode']
        self.activeModes = self.modes
        self.index = 0
    
    def incIndex(self):
        self.index = (self.index + 1) % len(self.modes)

    def reset(self):
        self.positions = ['reset', 'handClosed', 'handOpen', 'indexMiddle', 'indexMiddleRing', 'thumbIndexMiddle', 
        'pinkyIndexMiddle', 'thumb', 'index', 'pinky']
        self.mouseMode()
        self.lastCalled = {}
        for i in self.positions:
            self.lastCalled[i] = 0
    
    def setMode(self):
        if self.index == 0:
            self.mouseMode()
        elif self.index == 1:
            self.switchTabMode()
    
    def fillEmptyPos(self):
        for i in self.positions:
            if not i in self.settings:
                self.settings.update({i: self.keyboard.nothing})
    
    def mouseMode(self):
        self.settings = {
            'handOpen': self.switchMode, 
            'indexMiddle': self.keyboard.moveMouse,
            'thumbIndexMiddle': self.keyboard.click,
            'pinkyIndexMiddle': self.keyboard.rightClick}
        self.fillEmptyPos()
    
    def switchTabMode(self):
        self.settings = {
            'handOpen': self.switchMode, 
            'indexMiddle': self.keyboard.altTab,
            'indexMiddleRing': self.keyboard.winTab,
            'index': self.keyboard.enter,
            'thumb': self.keyboard.leftArrow,
            'pinky': self.keyboard.rightArrow}
        self.fillEmptyPos()

    def switchMode(self):
        self.incIndex()
        self.keyboard.alert(self.activeModes[self.index])
        self.setMode()
    
    def operate(self, key, optionalBool = True, cooldownMultiplier = 1):
        if time.time() - self.lastCalled[key] > self.cooldownTime * cooldownMultiplier and optionalBool:
            self.settings[key]()
            self.lastCalled[key] = time.time()

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    pos = positionDetector()
    s = settings()

    startTime = time.time()
    while True:
        if time.time() - startTime > 120:
            break
        # time.sleep(0.2)
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
            if time.time() - s.lastCalled['thumbIndexMiddle'] > s.cooldownTime and pos.isFinger(0):
                s.settings['thumbIndexMiddle']()
                s.lastCalled['thumbIndexMiddle'] = time.time()
            # Pinky is out, so right click
            elif time.time() - s.lastCalled['pinkyIndexMiddle'] > s.cooldownTime and pos.isFinger(4):
                s.settings['pinkyIndexMiddle']()
                s.lastCalled['pinkyIndexMiddle'] = time.time()
            s.settings['indexMiddle'](firstCall, newPos)
            s.lastCalled['indexMiddle'] = time.time()
        elif pos.areFingersStraight([1,2]):
            s.operate('indexMiddle')
        elif pos.areFingersStraight([1,2,3]):
            s.operate('indexMiddleRing')
        elif pos.areFingersStraight([0]):
            s.operate('thumb')
        elif pos.areFingersStraight([1]):
            s.operate('index')
        elif pos.areFingersStraight([4]):
            s.operate('pinky')
        elif pos.areFingersStraight([]):
            s.lastCalled['handClosed'] = time.time()
            print("hand closed")
        else:
            s.lastCalled['reset'] = time.time()
            print("nothing")

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()