import os
import pickle
import numpy as np
import cv2
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://face-attendance-system-caf12-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "face-attendance-system-caf12.appspot.com"
})

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('resources/background.png')
folderModePath = 'resources/mode'
modepath = os.listdir(folderModePath)

imgModeList = []
for path in modepath:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
# print(len(imgModeList))



#loading the encoding file

file = open("Encode.p",'rb')
encodelistknownwithIds = pickle.load(file)
file.close()
encodelistknown, studentList = encodelistknownwithIds
#print(studentList)

modeType = 0
counter = 0
id = -1

while True:
    success, img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facecurFrame = face_recognition.face_locations(imgS)
    encodecurFrame = face_recognition.face_encodings(imgS, facecurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    region_height, region_width = 633, 414
    for i in range(len(imgModeList)):

        mode_height, mode_width, _ = imgModeList[i].shape
        if region_height != mode_height or region_width != mode_width:
            imgModeList[i] = cv2.resize(imgModeList[i], (region_width, region_height))

        # Update the image assignment
        imgBackground[44:44 + region_height, 800:800 + region_width] = imgModeList[i]

    imgBackground[44:44 + region_height, 800:800 + region_width] = imgModeList[modeType]
    if facecurFrame:
        for encodeFace, faceLoc in zip(encodecurFrame, facecurFrame):
            matches = face_recognition.compare_faces(encodelistknown, encodeFace)
            faceDis = face_recognition.face_distance(encodelistknown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)
            if matches[matchIndex]:
                # print("Face Detected")
                # print(studentList[matchIndex])
                id = studentList[matchIndex]
                if counter == 0:
                    counter = 1
                    modeType = 1

            if counter!=0:

                if counter == 1:
                    studentInfo = db.reference(f'Students/{id}').get()

                    datetimeObject = datetime.strptime(studentInfo["last_attendance_time"],
                                                      "%Y-%m-%d %H:%M:%S")
                    seconds_elapsed = (datetime.now()-datetimeObject).total_seconds()
                    print(seconds_elapsed)
                    if seconds_elapsed>30:
                        ref = db.reference(f'Students/{id}')
                        studentInfo["attendance"]+=1

                        ref.child("attendance").set(studentInfo["attendance"])
                        ref.child("last_attendance_time").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        print(studentInfo)

                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + region_height, 800:800 + region_width] = imgModeList[modeType]

                if modeType!= 3:

                    if 10<counter<20:
                        modeType = 2
                    imgBackground[44:44 + region_height, 800:800 + region_width] = imgModeList[modeType]

                    if counter<=10:
                        cv2.putText(imgBackground, str(studentInfo['id']), (940, 393),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255),2)
                        cv2.putText(imgBackground, str(studentInfo['Branch']), (985, 486),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
                        (w,h),_ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX,1,2)
                        offset = (350-w)//2
                        cv2.putText(imgBackground, str(studentInfo['name']), (830 + offset, 275),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

                counter+=1

                if counter>=20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgBackground[44:44 + region_height, 800:800 + region_width] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0


    # imgBackground[44:44 + 633, 850:850 + 414] = imgModeList[0]

    #cv2.imshow("webcam", img)
    cv2.imshow("face Attendance", imgBackground)
    cv2.waitKey(1)









