import threading
import cv2
import time
import soundTest
import sendMail

'''
To detect motion we are just comparing the present frame with the previous frame and checking for the degree of 
difference in both of them and if it surpasses the threshold (min value above which we will call it a change  -
 can be adjusted) then we will call it as motion detected. 
'''
def detect_motion(prev_frame, frame):
    # Convert frames to grayscale for simpler comparison
    gray_prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate absolute difference between frames
    frame_diff = cv2.absdiff(gray_prev_frame, gray_frame)

    # Threshold for identifying motion (adjust as needed)
    thresh = cv2.threshold(frame_diff, 75, 255, cv2.THRESH_BINARY)[1]

    # Count number of non-zero pixels (indicating motion)
    count = cv2.countNonZero(thresh)

    # Set a threshold for the number of pixels to consider motion
    motion_threshold = 2500  # Adjust based on your camera and environment

    return count > motion_threshold


def capture_image(frame):
    # Capture the image with timestamp for unique filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"motion_detected.jpg"
    cv2.imwrite(filename, frame)
    print(f"Image captured and saved as: {filename}")


mail_sent = False  # should only send mail once and should capture the image only once


def initiate_camera():
    global mail_sent
    # Capture video from webcam
    cap = cv2.VideoCapture(0)

    # Check if webcam opened successfully
    if not cap.isOpened():
        print("Error opening webcam")
        exit()

    # Capture the first frame as reference
    ret, prev_frame = cap.read()

    detected_counter = 0  # count the detection
    counter_threshold = 12  # once counter reaches this number indicate that there is motion detected

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if frame was captured successfully
        if not ret:
            print("Error capturing frame")
            break

        # Detect motion
        motion_detected = detect_motion(prev_frame, frame)
        # Print message if motion detected
        if motion_detected:
            detected_counter += 1
            # run the alarm capture the ss and send the email with the attached picture
            if detected_counter < counter_threshold:
                sound_thread = threading.Thread(target=soundTest.alertSound)
                sound_thread.start()
                print("Motion detected!")
            else:  # can put some error handling in each of the functions to make code more reliable
                if not mail_sent:
                    capture_image(frame)
                    mail_status = sendMail.send_mail()  # can use thread to run it
                    if mail_status:
                        mail_sent = True
                        print("Sent the mail successfully !!")
                    else:
                        print("could not send the email!\nImage has been stored successfully !")
                else:
                    print("Already sent the mail !")
                # Release capture and close windows
                cap.release()
                cv2.destroyAllWindows()
                return 0
        # Update previous frame for next comparison
        prev_frame = frame
        # Display the resulting frame
        cv2.imshow('Live Feed', frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) == ord('q'):
            return 1  # will shut down the program


'''                MAIN                 '''

print("STARTING MOTION DETECTOR...")
print("Press q anytime to close the program..")
time.sleep(1)
while True:
    instance = initiate_camera()
    if instance == 1:
        print("Terminating....")
        print("Successfully closed webcam and windows")
        break
    else:
        print("Restarting camera in 4 secs...")
        time.sleep(4)
