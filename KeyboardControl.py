import pyautogui

class keyboardControl():
    def altTab (self):
        pyautogui.hotkey('alt', 'tab')

    def winTab(self):
        pyautogui.hotkey('win', 'tab')
    
    def click(self):
        pyautogui.click()