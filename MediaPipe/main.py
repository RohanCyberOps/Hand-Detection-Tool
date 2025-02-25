import cv2
import mediapipe as mp
import sys

# Initialize MediaPipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # Limit to detecting up to 2 hands
mp_drawing = mp.solutions.drawing_utils

# Start capturing from the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit(1)  # Exit with code 1 if webcam cannot be opened

print("Press 'q' to exit the program.")  # Instruction to exit

# Frame rate control
frame_rate = 30  # Desired frame rate (frames per second)
frame_delay = int(1000 / frame_rate)  # Delay in milliseconds

try:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            continue  # Skip to the next iteration if frame cannot be read

        # Flip the image horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB before processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and find hand landmarks
        results = hands.process(frame_rgb)

        # Draw hand landmarks and display confidence scores
        if results.multi_hand_landmarks:
            print(f"Number of hands detected: {len(results.multi_hand_landmarks)}")  # Debugging line
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Draw landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Display handedness (left/right) and confidence score
                if results.multi_handedness:
                    handedness = results.multi_handedness[idx]
                    label = handedness.classification[0].label  # Left or Right hand
                    confidence = handedness.classification[0].score  # Confidence score
                    print(f"Hand {idx + 1}: {label} hand, Confidence: {confidence:.2f}")

                    # Display the label and confidence on the frame
                    cv2.putText(frame, f"{label} hand ({confidence:.2f})",
                                (10, 30 + idx * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            print("No hand landmarks detected.")  # Informative message

        # Display the resulting frame
        cv2.imshow('Hand Gesture Detection', frame)

        # Frame rate control
        if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
            print("Exiting program...")
            break  # Exit the loop if 'q' is pressed

except KeyboardInterrupt:
    print("Program interrupted by user.")
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)  # Exit with code 1 for any exceptions

finally:
    cap.release()  # Release the webcam
    cv2.destroyAllWindows()  # Close all OpenCV windows
    print("Cleanup completed. Exiting program.")
    sys.exit(0)  # Exit with code 0 for successful termination