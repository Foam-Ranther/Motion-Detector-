# Motion-Detector-
This contains a motion detector that is built using OpenCV in python. 

WORKING -
Live feed is captured through camera and is processed by OpenCV on the go. Current and previous frame are compared and motion is detected based on the degree of difference between both the images. If the difference surpasses the threshold value then we call it as disturbance or motion detected.

FEATURES - 
1. On Motion detection, an alarm is triggered and after 10 triggererd frames, an email is sent to the user with attached image of the intrusion.


HOW TO USE - 

1. Just fork and dowload all the codes.
2. Create your own .env file in the same folder and set the send and reciever email with your choice.
3. Generate an app password for gmail through your google account setting (take help from internet) and put that also in .env to use
4. Install necessary libraries like openCV.
5. Run the Program and DONE !
