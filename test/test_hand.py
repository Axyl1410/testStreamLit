import cv2
import time
import mediapipe as mp

# Grabbing the Hand Model from Mediapipe and
# Initializing the Model
mp_hands = mp.solutions.hands
hands_model = mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initializing the drawing utils for drawing the hand landmarks on image
mp_drawing = mp.solutions.drawing_utils

# (0) in VideoCapture is used to connect to your computer's default camera
capture = cv2.VideoCapture(0)

# Initializing current time and previous time for calculating the FPS
previousTime = 0
currentTime = 0

while capture.isOpened():
    # Capture frame by frame
    ret, frame = capture.read()
    if not ret:
        break

    # Resizing the frame for better view
    frame = cv2.resize(frame, (800, 600))

    # Converting the frame from BGR to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Making predictions using hands model
    image.flags.writeable = False
    results = hands_model.process(image)
    image.flags.writeable = True

    # Converting back the RGB image to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Drawing Right hand Landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
            )

    # Calculating the FPS
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    # Displaying FPS on the image
    cv2.putText(image, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # Display the resulting image
    cv2.imshow("Hand Landmarks", image)

    # Enter key 'q' to break the loop
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# When all the process is done
# Release the capture and destroy all windows
capture.release()
cv2.destroyAllWindows()
