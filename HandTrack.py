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
    
    def reset(self):
        temp = ['handOpen', 'handClosed', 'indexMiddleOpen']
        self.settings = {'handOpen': self.keyboard.altTab, 'indexMiddleOpen': self.keyboard.click}
        self.lastCalled = {}
        for i in temp:
            self.lastCalled[i] = 0

    def swapDictElem(self, key1, key2):
        print(self.settings)
        if not key1 in self.settings or not key2 in self.settings:
            return
        temp = self.settings[key1]
        self.settings[key1] = self.settings[key2]
        self.settings[key2] = temp
        print(self.settings)
    
    # def operate(self, func):
        # elif time.time() - lastCooldownTrigger > cooldown:
        #     lastCooldownTrigger = time.time()

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    pos = positionDetector()
    s = settings()

    
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = detector.findHands(img, True)
        lmList = detector.findPosition(img)

        if len(lmList) == 0:
            lastCooldownTrigger = time.time()
            continue
        pos.update(lmList)
        

        # Everything that needs cooldown
        print(pos.isFinger(1))
        if False and pos.isHandOpen():
            if time.time() - s.lastCalled['handOpen'] > s.cooldownTime:
                s.settings['handOpen']()
                s.lastCalled['handOpen'] = time.time()
        elif pos.isFinger(1) and pos.isFinger(2):
            if time.time() - s.lastCalled['indexMiddleOpen'] > s.cooldownTime:
                s.settings['indexMiddleOpen']()
                s.lastCalled['indexMiddleOpen'] = time.time()
        
        # elif time.time() - lastCooldownTrigger > cooldown:
        #     lastCooldownTrigger = time.time()
        #     keyBoard.altTab()
        # if len(lmList) > 0:
            # print(pos.isFingerStraight(0), pos.isFingerStraight(1), pos.isFingerStraight(2), pos.isFingerStraight(3))
        # cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()