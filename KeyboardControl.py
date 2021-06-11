import pyautogui
import math

class keyboardControl():
    def __init__(self):
        pyautogui.FAILSAFE = False

    def alert(self, t):
        pyautogui.alert(text = t, title = 'mode change', button = 'OK', timeout=800)

    def nothing(self):
        pass

    def altTab (self):
        pyautogui.hotkey('alt', 'tab')

    def winTab(self):
        pyautogui.hotkey('win', 'tab')
    
    def rightArrow(self):
        pyautogui.press('right')

    def leftArrow(self):
        pyautogui.press('left')

    def click(self):
        pyautogui.click()
    
    def rightClick(self):
        pyautogui.rightClick()
    
    def moveMouse(self, firstMove, newPos):
        if firstMove:
            self.mousePos = newPos
        else:
            pyautogui.move(5 * int(self.mousePos[0] - newPos[0]), 5 * int(newPos[1] - self.mousePos[1]))
            self.mousePos = newPos
    
    def enter(self):
        pyautogui.press('enter')
    
    def volumeMute(self):
        pyautogui.press('volumemute')

    def volumeup(self):
        pyautogui.press('volumeup')

    def volumedown(self):
        pyautogui.press('volumedown')

