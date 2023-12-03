import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://face-attendance-system-caf12-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "face-attendance-system-caf12.appspot.com"
})

folderpath = 'images'
path = os.listdir(folderpath)
print(path)
imglist = []
studentlist = []
for path in path:
    imglist.append(cv2.imread(os.path.join(folderpath, path)))
    # print(path)
    # print(os.path.splitext(path))
    studentlist.append(os.path.splitext(path)[0])

    fileName = f'{folderpath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(studentlist)


def findEncoding(imageslist):
    encodelist = []
    for img in imageslist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)

    return encodelist




print("Encoding started")
encodelistknown = findEncoding(imglist)
encodelistknownwithIds = [encodelistknown,studentlist]
print("Encoding complete")
# print(encodelistknownwithIds)

file = open("Encode.p", 'wb')
pickle.dump(encodelistknownwithIds,file)
file.close()
print("file saved")







