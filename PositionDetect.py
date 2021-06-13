import math
import numpy as np
class positionDetector():
    def __init__(self):
        self.landmarks = None
        self.diff = []
        self.angles = []

    # Remove the IDs from the landmarks from mediapipe
    def removeID(self, p):
        return list(map(lambda x: x[1:], p))

    # Update the landmarks
    def update(self, landmarks):
        if len(landmarks) == 21:
            self.landmarks = landmarks
            self.points = self.removeID(landmarks)
            self.__process()

    def __process(self):
        self.diff = []
        self.angles = []
        # Determine the length between each joint on each finger
        for i in range(5):
            temp = []
            for j in range(4*i+1, 4*(i+1)):
                if j == 1:
                    continue
                temp.append(math.dist(self.points[j], self.points[j+1]))
            self.diff.append(temp)

        # Determine the direction each finger is pointing at
        for i in range(5):
            temp = []
            for j in range(4*i+1, 4*(i+1)):
                if j == 1:
                    continue
                temp.append(math.atan2(self.points[j+1][1] - self.points[j][1], self.points[j+1][0] - self.points[j][0]))
            self.angles.append(temp)
    
    def __inRange(self, val, min, max):
        return val >= min and val <= max

    # Determine whether a given finger is straight out or not
    # fingerNo: thumb = 0, index - 1, middle - 2, ring - 3, pinky - 4
    def isFingerStraightOut(self, fingerNo, wantOpen = False):
        fingerDiff = self.diff[fingerNo]
        fingerAngles = self.angles[fingerNo]
        isOpen = max(fingerDiff) == fingerDiff[0]
        isStraight = abs(max(fingerAngles) - min(fingerAngles)) < 0.35
        if fingerNo != 0:
            isOpen = isOpen and abs(fingerDiff[2] - fingerDiff[1]) < fingerDiff[1] * 0.4
        # Handle thumb
        if fingerNo == 0:
            isStraight = abs(max(fingerAngles) - min(fingerAngles)) < 0.45
            if wantOpen:
                    isStraight = isStraight and math.dist(self.points[4], self.points[5]) < math.dist(self.points[4], self.points[9])
                    isStraight = isStraight and math.dist(self.points[4], self.points[5]) > math.dist(self.points[5], self.points[9])
        return isOpen and isStraight
    
    # Returns true when the corresponding fingers from fingerNos is straight 
    # (i.e. fingerNos=[1,2] is index and middle finger are straight, rest are not)
    def areFingersStraight(self, fingerNos):
        if not self.landmarks:
            return False
        areFingers = True
        for i in range(5):
            temp = self.isFingerStraightOut(i, True) if i in fingerNos else not self.isFingerStraightOut(i, True)
            areFingers = areFingers and temp
        return areFingers
    
    # Returns true when all fingers on hand is open
    def isHandOpen(self):
        isOpen = True
        if not self.landmarks:
            return False
        for i in range(5):
            isOpen = isOpen and self.isFingerStraightOut(i, True)
        return isOpen
    
    # Returns true when all fingers on hand is closed
    def isHandClosed(self):
        isClosed = True
        if not self.landmarks:
            return False
        for i in range(5):
            isClosed = isClosed and not self.isFingerStraightOut(i)
        return isClosed

    # Returns true when only the specified finger is straight out (i.e. fingerNo=0 is curled fist with thumb out)
    def isFinger(self, fingerNo):
        if not self.landmarks:
            return False
        return self.isFingerStraightOut(fingerNo, True)
    
    # Returns true when the corresponding fingers from fingerNos is straight out
    # (i.e. fingerNos=[1,2] is index and middle finger are straight, regardless of other fingers)
    def isFingers(self, fingerNos):
        isFingers = True
        if not self.landmarks:
            return False
        for num in fingerNos:
            isFingers = isFingers and self.isFingerStraightOut(num, True)
        return isFingers


        
    