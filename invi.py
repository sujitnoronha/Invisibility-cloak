import cv2
import numpy as np
import time 
import random
import moviepy.editor as mp
import os

print("Move away from the video source to capture the background successfully")
time.sleep(3)
cap = cv2.VideoCapture(0)

for i in range(60):
    ret,background = cap.read()

background = np.flip(background, axis=1)
print()

frame_size = (720,480)

name = 'video_inp/Vid'+str(random.randint(0,100))+'.mp4'
video_in = cv2.VideoWriter(name, cv2.VideoWriter_fourcc('M','P','E','G'),20, (720, 480))


while(cap.isOpened()):
    ret, vid = cap.read()
    img = np.flip(vid,axis =1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.namedWindow("hsv")
    cv2.imshow("hsv", hsv)

    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    # Range for upper range

    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)

    mask = mask1+mask2

    mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))

    mask1 = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
    mask2 = cv2.bitwise_not(mask1)
    cv2.namedWindow("mask")
    cv2.imshow("mask", mask2)
    res1 = cv2.bitwise_and(img,img,mask=mask2)
    res2 = cv2.bitwise_and(background, background, mask = mask1)
    final_output = cv2.addWeighted(res1,1,res2,1,0)
    fimg = cv2.resize(final_output,(720, 480))
    video_in.write(fimg)
    cv2.imshow("invi",final_output)
    k = cv2.waitKey(1)
	
    if k == 27:
	    break


cv2.destroyAllWindows()
video_in.release()
cap.release()


audio = mp.AudioFileClip("theme.mp3")
print(name)
video1 = mp.VideoFileClip(name)
final = video1.set_audio(audio)

final.write_videofile("output/output.mp4",codec= 'mpeg4' ,audio_codec='libvorbis')
