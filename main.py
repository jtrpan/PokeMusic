from PIL import ImageGrab
import numpy as np
import cv2
import pytesseract
import platform
from random import choice
from screeninfo import get_monitors

monitor = get_monitors()[0]  # Get the primary monitor
screen_width = monitor.width
screen_height = monitor.height

# Map each gameplay situation to its corresponding music files
music_files = {
    "Title Screen": [f"music/title{i}.wav" for i in range(1, 7)],
    "Open World (Exploration)": [f"music/city{i}.wav" for i in range(1, 16)] + [f"music/route{i}.wav" for i in
                                                                                range(1, 13)],
    "Wild Pokemon Battle": [f"music/wild{i}.wav" for i in range(1, 5)],
    "Trainer Battle": [f"music/trainer{i}.wav" for i in range(1, 5)],
    "Rival Battle": [f"music/rival{i}.wav" for i in range(1, 4)],
    "Gym Leader Battle": [f"music/gym{i}.wav" for i in range(1, 8)],
    "Elite Four Battle": [f"music/elite{i}.wav" for i in range(1, 5)],
    "Champion Battle": [f"music/champ{i}.wav" for i in range(1, 4)],
    "Organization (Rocket/Galactic) Grunt Battle": [],  # Add files when available
    "Organization Commander Battle": [f"music/commander{i}.wav" for i in range(1, 2)],
    "Organization Boss Battle": [f"music/boss{i}.wav" for i in range(1, 2)],
    "Legendary Pokemon Battle": ["music/zinnia.wav"],  # Add more files if available
}


def get_platform():
    if platform.system() == "Windows":
        # Windows-specific code
        # pytesseract.pytesseract.tesseract_cmd z = r'D:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
        # pytesseract.pytesseract.tesseract_cmd = r'/Users/jtrpan/Games/Nintendo/PokeMusic/Tesseract-OCR'
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
    elif platform.system() == "Darwin":
        # macOS-specific code
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
        pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'


def play_music(situation):
    # Randomly select a music file from the corresponding list
    sound_file = choice(music_files[situation])
    if platform.system() == "Windows":
        # Windows-specific code
        import winsound
        winsound.PlaySound(sound_file, winsound.SND_LOOP + winsound.SND_ASYNC)
    elif platform.system() == "Darwin":
        # macOS-specific code
        import subprocess
        subprocess.Popen(["afplay", sound_file])


def roi(img, vertices):
    # blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked


def identify(text):
    situations = {
        "Wild Pokemon Battle": ["A wild", "appeared"],
        "Trainer Battle": ["You are challenged", "are challenged by", "challenged by"],
        "Gym Leader Battle": ["Leader", "Boss", "Gym", "Champion", "Elite", "Admin"],
        "Rival Battle": ["Rival"],
        "Open World (Exploration)": ["Save your", "your game", "game with", "your progress", "A device", "device that",
                                     "that records", "upon meeting", "meeting or", "Check and", "and organize",
                                     "traveling with", "with you", "Equipped with", "with pockets", "pockets for",
                                     "you bought", "bought, received", "Check your", "your money", "Got away",
                                     "away safely"]
    }

    for situation, keywords in situations.items():
        if any(keyword in text for keyword in keywords):
            return situation

    return None  # Return None if no situation is identified


def musicPlayer(situation, keepPlaying):
    if situation is None:
        return
    if (keepPlaying):
        return
    else:
        play_music(situation)
    return


def get_player_mode():
    while True:
        print('Enter 0 for text detection, or 1 for manual control')
        try:
            playerMode = int(input())
            if playerMode in [0, 1]:
                return playerMode
            else:
                print("Invalid input. Please enter 0 or 1.")
        except ValueError:
            print("Please enter a valid number.")


def main():
    situation = 6
    lastSit = 7
    firstEntry = True

    get_platform()

    playerMode = get_player_mode()
    if playerMode == 0:
        print('Text detection selected.')
    else:
        print('Manual control selected.')
    while True:
        if playerMode == 0:
            auto_bbox = (0, screen_height // 2, screen_width, screen_height)
            img = ImageGrab.grab(bbox=auto_bbox)  # bbox specifies specific region (bbox= x,y,width,height)
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
            situation = identify(myText)
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
