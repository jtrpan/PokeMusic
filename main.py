import time
import atexit
import cv2
import pytesseract
import platform
import Quartz
import subprocess
import numpy as np
from PIL import ImageGrab
from random import choice
from screeninfo import get_monitors

# Global variable to hold the current music process
current_music_process = None

# Global variable to remember the last situation
lastSit = ""

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
    "Organization (Rocket/Galactic) Grunt Battle": [f"music/grunt{i}.wav" for i in range(1, 2)],
    "Organization Commander Battle": [f"music/commander{i}.wav" for i in range(1, 2)],
    "Organization Boss Battle": [f"music/boss{i}.wav" for i in range(1, 2)],
    "Legendary Pokemon Battle": [f"music/epic{i}.wav" for i in range(1, 2)],
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


def get_vba_window():
    window_list = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    for window in window_list:
        window_title = window.get('kCGWindowName', 'Unknown')
        if "VisualBoyAdvance" in window_title:
            return window  # return the actual window object, not just the title
    return None  # return None if no such window is found


def default_vba_window():
    monitor = get_monitors()[0]  # Get the primary monitor
    screen_width = monitor.width
    screen_height = monitor.height
    bbox = (0, screen_height // 2, screen_width // 2, screen_height)
    return bbox


def capture_text_region(x, y, width, height):
    # Assuming the text appears in the bottom 1/3 of the screen.
    # Adjust the starting y-coordinate and the height accordingly.
    text_region_height = height // 3  # Capture bottom 1/3
    text_region_y = y + (2 * height // 3)  # Start capturing from here

    # You might need to adjust this area slightly, depending on the exact layout of your game screen.
    # The goal is to create a new bounding box (bbox) that encompasses just the area where the text appears.
    text_bbox = (x, text_region_y, x + width, text_region_y + text_region_height)

    # Now, use this bbox to capture the screen
    img = ImageGrab.grab(bbox=text_bbox)  # bbox specifies specific region (bbox= x,y,width,height)
    return img


def playMusic(situation):
    global current_music_process  # Declare that we are using the global variable

    # Randomly select a music file from the corresponding list
    sound_file = choice(music_files[situation])

    if current_music_process is not None:
        current_music_process.terminate()
        # Wait for a bit to see if the process terminates
        time.sleep(0.5)  # wait for 500 milliseconds
        if current_music_process.poll() is None:  # None means it's still running
            current_music_process.kill()  # force kill
            current_music_process.wait()  # wait for the process to end

    # Now that any previous music has been stopped, start the new soundtrack
    if platform.system() == "Windows":
        # Windows-specific code
        import winsound
        winsound.PlaySound(sound_file, winsound.SND_LOOP + winsound.SND_ASYNC)
    elif platform.system() == "Darwin":
        # macOS-specific code
        current_music_process = subprocess.Popen(["afplay", sound_file])


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
                                     "are traveling", "traveling with", "with you", "Equipped with", "with pockets",
                                     "pockets for", "you bought", "bought, received", "Check your", "your money",
                                     "Got away", "away safely", "to save", "save the", "the game"]
    }

    for situation, keywords in situations.items():
        if any(keyword in text for keyword in keywords):
            return situation

    return None  # Return None if no situation is identified


def musicPlayer(situation):
    global lastSit  # This should be declared globally to remember the last situation

    if situation is None:
        return

    # Check if the situation has changed from the last one
    if situation != lastSit:
        # Update the last situation
        lastSit = situation
        print(f"Updated situation: {situation}")  # For debugging purposes

        # Play the new track since the situation has changed
        playMusic(situation)
    else:
        # If the situation hasn't changed, we don't need to do anything
        print(f"Still in the same situation: {situation}")  # For debugging purposes


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


def manual_mode_selection():
    print("\nManual control selected. Please choose a situation:")
    print("0: Explore (Open World)")
    print("1: Wild Pokemon Battle")
    print("2: Gym Leader Battle")
    print("3: Rival Battle")
    print("4: Trainer Battle")
    print("5: Elite Four Battle")
    print("6: Return to Title Screen")
    print("7: Exit Manual Mode")  # If you want to provide an option to go back to the main menu

    while True:  # This loop continues until a valid input is received
        try:
            user_input = int(input("Enter a number corresponding to the situation: "))
            if 0 <= user_input <= 7:  # Check if the input is within the valid range
                return user_input
            else:
                print("Invalid selection. Please enter a number between 0 and 7.")
        except ValueError:  # Non-integer input would raise a ValueError
            print("Invalid input. Please enter a number.")


def cleanup():
    global current_music_process
    if current_music_process:
        # If there's a music process running, terminate it
        current_music_process.terminate()
        current_music_process = None
    print("Cleanup completed. Exiting program.")


# Register the cleanup function to be called on exit
atexit.register(cleanup)


def main():
    global current_music_process  # Reference the global variable
    global music_files  # Make sure music_files is accessible

    situation = "Title Screen"
    musicPlayer(situation)

    lastSit = ""
    firstEntry = True
    config = '-l eng --oem 1 --psm 3'  # configurations

    frame_skip = 5  # for instance, adjust as needed
    counter = 0

    get_platform()
    playerMode = get_player_mode()

    if playerMode == 0:
        print('Text detection selected.')
    else:
        print('Manual control selected.')
    while True:
        if playerMode == 0:
            if counter % frame_skip == 0:
                vba_window = get_vba_window()
                if vba_window:
                    # The window details are in the dictionary, under the 'kCGWindowBounds' key
                    bounds = vba_window.get('kCGWindowBounds')
                    x = int(bounds['X'])
                    y = int(bounds['Y'])
                    width = int(bounds['Width'])
                    height = int(bounds['Height'] - 20)
                else:
                    print("No VisualBoyAdvance window found")
                    # Handle the case where the window is not found, perhaps by waiting or exiting
                    (x, y, width, height) = default_vba_window()

                # Define the vertices of the polygon (rectangle in this case) based on the VBA window dimensions.
                # The coordinates are: top-left, bottom-left, bottom-right, top-right
                vertices = np.array([
                    [x, y],
                    [x, y + height],
                    [x + width, y + height],
                    [x + width, y]
                ], np.int32)
                # vertices = np.array([[20, 900], [20, 660], [1000, 660], [1000, 900]], np.int32)
                auto_bbox = (x, y, x + width, y + height)
                # img = ImageGrab.grab(bbox=auto_bbox)  # bbox specifies specific region (bbox= x,y,width,height)

                # Capture only the region where the text is expected to be
                img = capture_text_region(x, y, width, height)

                # Convert PIL image to OpenCV format
                img_np = np.array(img)
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

                # Display the original image with the rectangle
                # cv2.imshow("Original with BBox", img_np)
                frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

                # Process with Canny
                canny_img = cv2.Canny(frame, threshold1=100, threshold2=350)

                # Process with thresholding
                ret, thresh_img = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)

                # Combine both images (you might need to adjust how you combine based on testing)
                processed_img = cv2.bitwise_or(canny_img, thresh_img)

                # Define the vertices of the polygon (rectangle in this case) based on the VBA window dimensions.
                # The coordinates are: top-left, bottom-left, bottom-right, top-right
                vertices = np.array([
                    [x, y],
                    [x, y + height],
                    [x + width, y + height],
                    [x + width, y]
                ], np.int32)
                # vertices = np.array([[20, 900], [20, 660], [1000, 660], [1000, 900]], np.int32)

                processed_img = roi(processed_img, [vertices])

                # cv2.imshow("Capture", processed_img)

                # Add a waitKey to keep the window open
                cv2.waitKey(1)

                # PyTesseract
                myText = pytesseract.image_to_string(processed_img, config=config)

                # Inside your main loop where you call musicPlayer
                situation = identify(myText)  # This identifies the current situation based on the text

                # Call the music player function to handle music playing
                musicPlayer(situation)
            counter += 1
        else:
            situation_mapping = {
                0: "Open World (Exploration)",
                1: "Wild Pokemon Battle",
                2: "Gym Leader Battle",
                3: "Rival Battle",
                4: "Trainer Battle",
                5: "Elite Four Battle",
                6: "Title Screen",
                7: "Exit"  # Handle the exit condition in your main loop
            }

            user_choice = manual_mode_selection()  # This function will return only when valid input is entered

            if user_choice == 7:
                print("Exiting manual mode...")

                break  # This will exit the current loop, you might want to change the flow depending on your needs

            situation = situation_mapping[user_choice]

            musicPlayer(situation)  # Play music based on the user's choice


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, perform any additional logging or error handling here

    # No need to explicitly call cleanup() here; it will be called automatically upon exit
import time
import atexit
import cv2
import pytesseract
import platform
import Quartz
import subprocess
import numpy as np
from PIL import ImageGrab
from random import choice
from screeninfo import get_monitors

# Global variable to hold the current music process
current_music_process = None

# Global variable to remember the last situation
lastSit = ""

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
    "Organization (Rocket/Galactic) Grunt Battle": [f"music/grunt{i}.wav" for i in range(1, 2)],
    "Organization Commander Battle": [f"music/commander{i}.wav" for i in range(1, 2)],
    "Organization Boss Battle": [f"music/boss{i}.wav" for i in range(1, 2)],
    "Legendary Pokemon Battle": [f"music/epic{i}.wav" for i in range(1, 2)],
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


def get_vba_window():
    window_list = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    for window in window_list:
        window_title = window.get('kCGWindowName', 'Unknown')
        if "VisualBoyAdvance" in window_title:
            return window  # return the actual window object, not just the title
    return None  # return None if no such window is found


def default_vba_window():
    monitor = get_monitors()[0]  # Get the primary monitor
    screen_width = monitor.width
    screen_height = monitor.height
    bbox = (0, screen_height // 2, screen_width // 2, screen_height)
    return bbox


def capture_text_region(x, y, width, height):
    # Assuming the text appears in the bottom 1/3 of the screen.
    # Adjust the starting y-coordinate and the height accordingly.
    text_region_height = height // 3  # Capture bottom 1/3
    text_region_y = y + (2 * height // 3)  # Start capturing from here

    # You might need to adjust this area slightly, depending on the exact layout of your game screen.
    # The goal is to create a new bounding box (bbox) that encompasses just the area where the text appears.
    text_bbox = (x, text_region_y, x + width, text_region_y + text_region_height)

    # Now, use this bbox to capture the screen
    img = ImageGrab.grab(bbox=text_bbox)  # bbox specifies specific region (bbox= x,y,width,height)
    return img


def playMusic(situation):
    global current_music_process  # Declare that we are using the global variable

    # Randomly select a music file from the corresponding list
    sound_file = choice(music_files[situation])

    if current_music_process is not None:
        current_music_process.terminate()
        # Wait for a bit to see if the process terminates
        time.sleep(0.5)  # wait for 500 milliseconds
        if current_music_process.poll() is None:  # None means it's still running
            current_music_process.kill()  # force kill
            current_music_process.wait()  # wait for the process to end

    # Now that any previous music has been stopped, start the new soundtrack
    if platform.system() == "Windows":
        # Windows-specific code
        import winsound
        winsound.PlaySound(sound_file, winsound.SND_LOOP + winsound.SND_ASYNC)
    elif platform.system() == "Darwin":
        # macOS-specific code
        current_music_process = subprocess.Popen(["afplay", sound_file])


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
                                     "are traveling", "traveling with", "with you", "Equipped with", "with pockets",
                                     "pockets for", "you bought", "bought, received", "Check your", "your money",
                                     "Got away", "away safely", "to save", "save the", "the game"]
    }

    for situation, keywords in situations.items():
        if any(keyword in text for keyword in keywords):
            return situation

    return None  # Return None if no situation is identified


def musicPlayer(situation):
    global lastSit  # This should be declared globally to remember the last situation

    if situation is None:
        return

    # Check if the situation has changed from the last one
    if situation != lastSit:
        # Update the last situation
        lastSit = situation
        print(f"Updated situation: {situation}")  # For debugging purposes

        # Play the new track since the situation has changed
        playMusic(situation)
    else:
        # If the situation hasn't changed, we don't need to do anything
        print(f"Still in the same situation: {situation}")  # For debugging purposes


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


def manual_mode_selection():
    print("\nManual control selected. Please choose a situation:")
    print("0: Explore (Open World)")
    print("1: Wild Pokemon Battle")
    print("2: Gym Leader Battle")
    print("3: Rival Battle")
    print("4: Trainer Battle")
    print("5: Elite Four Battle")
    print("6: Return to Title Screen")
    print("7: Exit Manual Mode")  # If you want to provide an option to go back to the main menu

    while True:  # This loop continues until a valid input is received
        try:
            user_input = int(input("Enter a number corresponding to the situation: "))
            if 0 <= user_input <= 7:  # Check if the input is within the valid range
                return user_input
            else:
                print("Invalid selection. Please enter a number between 0 and 7.")
        except ValueError:  # Non-integer input would raise a ValueError
            print("Invalid input. Please enter a number.")


def cleanup():
    global current_music_process
    if current_music_process:
        # If there's a music process running, terminate it
        current_music_process.terminate()
        current_music_process = None
    print("Cleanup completed. Exiting program.")


# Register the cleanup function to be called on exit
atexit.register(cleanup)


def main():
    global current_music_process  # Reference the global variable
    global music_files  # Make sure music_files is accessible

    situation = "Title Screen"
    musicPlayer(situation)

    lastSit = ""
    firstEntry = True
    config = '-l eng --oem 1 --psm 3'  # configurations

    frame_skip = 5  # for instance, adjust as needed
    counter = 0

    get_platform()
    playerMode = get_player_mode()

    if playerMode == 0:
        print('Text detection selected.')
    else:
        print('Manual control selected.')
    while True:
        if playerMode == 0:
            if counter % frame_skip == 0:
                vba_window = get_vba_window()
                if vba_window:
                    # The window details are in the dictionary, under the 'kCGWindowBounds' key
                    bounds = vba_window.get('kCGWindowBounds')
                    x = int(bounds['X'])
                    y = int(bounds['Y'])
                    width = int(bounds['Width'])
                    height = int(bounds['Height'] - 20)
                else:
                    print("No VisualBoyAdvance window found")
                    # Handle the case where the window is not found, perhaps by waiting or exiting
                    (x, y, width, height) = default_vba_window()

                # Define the vertices of the polygon (rectangle in this case) based on the VBA window dimensions.
                # The coordinates are: top-left, bottom-left, bottom-right, top-right
                vertices = np.array([
                    [x, y],
                    [x, y + height],
                    [x + width, y + height],
                    [x + width, y]
                ], np.int32)
                # vertices = np.array([[20, 900], [20, 660], [1000, 660], [1000, 900]], np.int32)
                auto_bbox = (x, y, x + width, y + height)
                # img = ImageGrab.grab(bbox=auto_bbox)  # bbox specifies specific region (bbox= x,y,width,height)

                # Capture only the region where the text is expected to be
                img = capture_text_region(x, y, width, height)

                # Convert PIL image to OpenCV format
                img_np = np.array(img)
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

                # Display the original image with the rectangle
                # cv2.imshow("Original with BBox", img_np)
                frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

                # Process with Canny
                canny_img = cv2.Canny(frame, threshold1=100, threshold2=350)

                # Process with thresholding
                ret, thresh_img = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)

                # Combine both images (you might need to adjust how you combine based on testing)
                processed_img = cv2.bitwise_or(canny_img, thresh_img)

                # Define the vertices of the polygon (rectangle in this case) based on the VBA window dimensions.
                # The coordinates are: top-left, bottom-left, bottom-right, top-right
                vertices = np.array([
                    [x, y],
                    [x, y + height],
                    [x + width, y + height],
                    [x + width, y]
                ], np.int32)
                # vertices = np.array([[20, 900], [20, 660], [1000, 660], [1000, 900]], np.int32)

                processed_img = roi(processed_img, [vertices])

                # cv2.imshow("Capture", processed_img)

                # Add a waitKey to keep the window open
                cv2.waitKey(1)

                # PyTesseract
                myText = pytesseract.image_to_string(processed_img, config=config)

                # Inside your main loop where you call musicPlayer
                situation = identify(myText)  # This identifies the current situation based on the text

                # Call the music player function to handle music playing
                musicPlayer(situation)
            counter += 1
        else:
            situation_mapping = {
                0: "Open World (Exploration)",
                1: "Wild Pokemon Battle",
                2: "Gym Leader Battle",
                3: "Rival Battle",
                4: "Trainer Battle",
                5: "Elite Four Battle",
                6: "Title Screen",
                7: "Exit"  # Handle the exit condition in your main loop
            }

            user_choice = manual_mode_selection()  # This function will return only when valid input is entered

            if user_choice == 7:
                print("Exiting manual mode...")

                break  # This will exit the current loop, you might want to change the flow depending on your needs

            situation = situation_mapping[user_choice]

            musicPlayer(situation)  # Play music based on the user's choice


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, perform any additional logging or error handling here

    # No need to explicitly call cleanup() here; it will be called automatically upon exit
