import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

# Added the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

scores = [0, 0]  # [AI, player]

imgAI = None
round_start_time = time.time()
winner_message = ""
stateResults = False  # Initialize stateResults

# Added the bg

# Wait for 's' key press to start the game
while True:
    success, img = cap.read()
    cv2.putText(img, "Press 's' to start the game", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("BG", img)
    key = cv2.waitKey(1)
    if key == ord('s'):
        break

while True:
    # Start the next round automatically after 4 seconds or when the timer hits 0
    if time.time() - round_start_time > 4 or time.time() - round_start_time == 0:
        round_start_time = time.time()
        winner_message = ""
        stateResults = False  # Reset stateResults at the beginning of each round

    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    # Scaled the image
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)

    if stateResults is False:
        # provides with an array of 5 values representing each finger
        if hands:
            playerMove = None
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            # player part
            if fingers == [0, 0, 0, 0, 0]:  # rock
                playerMove = 1
            if fingers == [1, 1, 1, 1, 1]:  # paper
                playerMove = 2
            if fingers == [0, 1, 1, 0, 0]:  # scissors
                playerMove = 3

            randomNumber = random.randint(1, 3)
            imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
            imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

            # Player Wins
            if (playerMove == 1 and randomNumber == 3) or \
                    (playerMove == 2 and randomNumber == 1) or \
                    (playerMove == 3 and randomNumber == 2):
                scores[1] += 1

            # AI Wins
            if (playerMove == 3 and randomNumber == 1) or \
                    (playerMove == 1 and randomNumber == 2) or \
                    (playerMove == 2 and randomNumber == 3):
                scores[0] += 1

            # Check if either AI or player reached 5 points
            if scores[0] >= 5:
                # AI wins
                winner_message = "AI wins!"
            elif scores[1] >= 5:
                # Player wins
                winner_message = "Player wins!"

            # Set state for next round
            stateResults = True

    imgBG[234:654, 795:1195] = imgScaled

    if stateResults:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # Display timer
    timer_text = "Timer: " + str(int(4 - (time.time() - round_start_time)))
    timer_text_size = cv2.getTextSize(timer_text, cv2.FONT_HERSHEY_SIMPLEX, 1.6, 4)[0]  # Reduced font scale by 20%
    timer_text_x = 795 - (timer_text_size[0] + 40)  # Adjusted position to the left of the orange box
    timer_text_y = 234 + (210 + timer_text_size[1] // 2) - 40  # Adjusted position 1 cm up
    cv2.putText(imgBG, timer_text, (timer_text_x, timer_text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 0), 4)

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 3.2, (0, 0, 0), 6)  # Reduced font scale by 20%
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 3.2, (0, 0, 0), 6)  # Reduced font scale by 20%

    # Display winner message
    if winner_message:
        winner_message_size = cv2.getTextSize(winner_message, cv2.FONT_HERSHEY_SIMPLEX, 1.4, 4)[0]  # Reduced font scale by 20%
        winner_message_x = (imgBG.shape[1] - winner_message_size[0]) // 2 + 20  # Shifted horizontally to the right
        winner_message_y = 200
        cv2.putText(imgBG, winner_message, (winner_message_x, winner_message_y), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 4)
        cv2.imshow("BG", imgBG)
        cv2.waitKey(3000)  # Display winner message for 3 seconds
        break

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)

    # Exit the game if 'q' is pressed
    if key == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
