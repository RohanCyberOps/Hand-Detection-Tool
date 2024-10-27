import cv2
import mediapipe as mp
import sys

# Initialize MediaPipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Start capturing from the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit(1)  # Exit with code 1 if webcam cannot be opened

print("Press 'q' to exit the program.")  # Instruction to exit

try:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame. Ret:", ret)
            continue  # Skip to the next iteration if frame cannot be read

        # Flip the image horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB before processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and find hand landmarks
        results = hands.process(frame_rgb)

        # Draw hand landmarks
        if results.multi_hand_landmarks:
            print(f"Number of hands detected: {len(results.multi_hand_landmarks)}")  # Debugging line
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        else:
            print("No hand landmarks detected.")  # Informative message

        # Display the resulting frame
        cv2.imshow('Hand Gesture Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting program...")
            break  # Exit the loop if 'q' is pressed

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)  # Exit with code 1 for any exceptions

finally:
    cap.release()  # Release the webcam
    cv2.destroyAllWindows()  # Close all OpenCV windows
    print("Cleanup completed. Exiting program.")
    sys.exit(0)  # Exit with code 0 for successful termination
