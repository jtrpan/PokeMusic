from PIL import ImageGrab
from random import randint
import numpy as np
import cv2
import pytesseract
import winsound

# pytesseract.pytesseract.tesseract_cmd z = r'D:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'/Users/jtrpan/Games/Nintendo/PokeMusic/Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'


def roi(img, vertices):
    # blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked


def identify(text, situation):
    if (situation == 0):
        if ("What will" in text) or ("do?" in text):
            situation = 5

    if ("A wild" in text) or ("appeared" in text):
        situation = 1
    elif ("You are" in text) or ("are challenged" in text) or ("challenged by" in text):
        if ("Leader" in text) or ("Boss" in text) or ("Gym" in text) or ("Champion" in text) or ("Elite" in text) or (
                "Admin" in text):
            situation = 2
        elif ("Rival" in text):
            situation = 3
        else:
            situation = 4
    elif ("Save your" in text) or \
            ("your game" in text) or \
            ("game with" in text) or \
            ("your progress" in text) or \
            ("A device" in text) or \
            ("device that" in text) or \
            ("that records" in text) or \
            ("upon meeting" in text) or \
            ("meeting or" in text) or \
            ("Check and" in text) or \
            ("and organize" in text) or \
            ("traveling with" in text) or \
            ("with you" in text) or \
            ("Equipped with" in text) or \
            ("with pockets" in text) or \
            ("pockets for" in text) or \
            ("you bought" in text) or \
            ("bought, received" in text) or \
            ("Check your" in text) or \
            ("your money" in text) or \
            ("Got away" in text) or \
            ("away safely" in text):
        situation = 0

    return situation


def musicPlayer(situation, keepPlaying):
    if (keepPlaying):
        return
    else:
        if (situation == 0):
            picker = randint(1, 28)
            if picker == 1:
                winsound.PlaySound(r'music/city1.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 2:
                winsound.PlaySound(r'music/city2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 3:
                winsound.PlaySound(r'music/city2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 4:
                winsound.PlaySound(r'music/city3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 5:
                winsound.PlaySound(r'music/city4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 6:
                winsound.PlaySound(r'music/city5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 7:
                winsound.PlaySound(r'music/city6.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 8:
                winsound.PlaySound(r'music/city7.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 9:
                winsound.PlaySound(r'music/city8.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 10:
                winsound.PlaySound(r'music/city9.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 11:
                winsound.PlaySound(r'music/city10.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 12:
                winsound.PlaySound(r'music/city11.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 13:
                winsound.PlaySound(r'music/city12.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 14:
                winsound.PlaySound(r'music/city13.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 15:
                winsound.PlaySound(r'music/city14.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 16:
                winsound.PlaySound(r'music/city15.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 17:
                winsound.PlaySound(r'music/route1.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 18:
                winsound.PlaySound(r'music/route2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 19:
                winsound.PlaySound(r'music/route3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 20:
                winsound.PlaySound(r'music/route4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 21:
                winsound.PlaySound(r'music/route5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 22:
                winsound.PlaySound(r'music/route6.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 23:
                winsound.PlaySound(r'music/route7.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 24:
                winsound.PlaySound(r'music/route8.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 25:
                winsound.PlaySound(r'music/route9.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 26:
                winsound.PlaySound(r'music/route10.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 27:
                winsound.PlaySound(r'music/route11.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 28:
                winsound.PlaySound(r'music/route12.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

        elif (situation == 1):
            picker = randint(1, 4)
            if picker == 1:
                winsound.PlaySound(r'music/wildG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 2:
                winsound.PlaySound(r'music/wildG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 3:
                winsound.PlaySound(r'music/wildG4.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 4:
                winsound.PlaySound(r'music/wildG5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

        elif (situation == 2):
            picker = randint(1, 17)
            if picker == 1:
                winsound.PlaySound(r'music/champG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 2:
                winsound.PlaySound(r'music/champG4.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 3:
                winsound.PlaySound(r'music/champG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 4:
                winsound.PlaySound(r'music/eliteG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 5:
                winsound.PlaySound(r'music/eliteG5.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 6:
                winsound.PlaySound(r'music/eliteG5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 7:
                winsound.PlaySound(r'music/gymG3.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 8:
                winsound.PlaySound(r'music/gymG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 9:
                winsound.PlaySound(r'music/gymG3.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 10:
                winsound.PlaySound(r'music/gymG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 11:
                winsound.PlaySound(r'music/gymG4.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 12:
                winsound.PlaySound(r'music/gymG5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 13:
                winsound.PlaySound(r'music/gymG5.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 14:
                winsound.PlaySound(r'music/gymG8.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 15:
                winsound.PlaySound(r'music/marnie.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 16:
                winsound.PlaySound(r'music/zinnia.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 17:
                winsound.PlaySound(r'music/zinnia2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

        elif (situation == 3):
            picker = randint(1, 3)
            if picker == 1:
                winsound.PlaySound(r'music/rivalG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 2:
                winsound.PlaySound(r'music/rivalG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 3:
                winsound.PlaySound(r'music/rivalG5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

        elif (situation == 4):
            picker = randint(1, 4)
            if picker == 1:
                winsound.PlaySound(r'music/trainerG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 2:
                winsound.PlaySound(r'music/trainerG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 3:
                winsound.PlaySound(r'music/trainerG4.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 4:
                winsound.PlaySound(r'music/trainerG5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

        elif (situation == 5):
            picker = randint(1, 26)
            if picker == 1:
                winsound.PlaySound(r'music/champG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 2:
                winsound.PlaySound(r'music/champG4.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 3:
                winsound.PlaySound(r'music/champG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 4:
                winsound.PlaySound(r'music/eliteG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 5:
                winsound.PlaySound(r'music/eliteG5.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 6:
                winsound.PlaySound(r'music/eliteG5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 7:
                winsound.PlaySound(r'music/gymG3.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 8:
                winsound.PlaySound(r'music/gymG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 9:
                winsound.PlaySound(r'music/gymG3.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 10:
                winsound.PlaySound(r'music/gymG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 11:
                winsound.PlaySound(r'music/gymG4.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 12:
                winsound.PlaySound(r'music/gymG5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 13:
                winsound.PlaySound(r'music/gymG5.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 14:
                winsound.PlaySound(r'music/gymG8.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 15:
                winsound.PlaySound(r'music/marnie.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 16:
                winsound.PlaySound(r'music/zinnia.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 17:
                winsound.PlaySound(r'music/zinnia2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 18:
                winsound.PlaySound(r'music/rivalG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 19:
                winsound.PlaySound(r'music/rivalG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 20:
                winsound.PlaySound(r'music/rivalG5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 21:
                winsound.PlaySound(r'music/trainerG3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 22:
                winsound.PlaySound(r'music/trainerG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 23:
                winsound.PlaySound(r'music/trainerG4.2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 24:
                winsound.PlaySound(r'music/trainerG5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 25:
                winsound.PlaySound(r'music/bossG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 26:
                winsound.PlaySound(r'music/commanderG4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

        elif (situation == 6):
            picker = randint(1, 6)
            if picker == 1:
                winsound.PlaySound(r'music/title1.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 2:
                winsound.PlaySound(r'music/title2.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 3:
                winsound.PlaySound(r'music/title3.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 4:
                winsound.PlaySound(r'music/title4.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 5:
                winsound.PlaySound(r'music/title5.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
            elif picker == 6:
                winsound.PlaySound(r'music/title6.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

    return


def main():
    situation = 6
    lastSit = 7
    firstEntry = True
    print('Enter 0 for text detection, or other for manual control')
    playerMode = int(input())
    if playerMode == 0:
        print('Text detection selected.')
    else:
        print('Manual control selected.')
    while True:
        if playerMode == 0:
            img = ImageGrab.grab(bbox=(0, 0, 1200, 850))  # bbox specifies specific region (bbox= x,y,width,height)
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
            processed_img = cv2.Canny(frame, threshold1=100, threshold2=350)
            vertices = np.array([[20, 900], [20, 660], [1000, 660], [1000, 900],
                                 ], np.int32)
            processed_img = roi(processed_img, [vertices])
            cv2.imshow("Capture", processed_img)
            # configurations
            config = '-l eng --oem 1 --psm 3'
            # PyTesseract
            myText = pytesseract.image_to_string(processed_img, config=config)
            situation = identify(myText, situation)
            if situation != lastSit:
                lastSit = situation
                musicPlayer(situation, False)
                print(myText)
            else:
                musicPlayer(situation, True)
        else:
            if firstEntry:
                situation = 6
                firstEntry = False
                musicPlayer(situation, False)
            else:
                print(
                    'Enter:'
                    '\n0 for Explore'
                    '\n1 for Wild'
                    '\n2 for Leader'
                    '\n3 for Rival'
                    '\n4 for Trainer'
                    '\n5 for Battle'
                    '\n6 for Title'
                )
                situation = int(input())
                if situation != lastSit:
                    lastSit = situation
                    musicPlayer(situation, False)
                else:
                    musicPlayer(situation, True)


if __name__ == "__main__":
    main()
