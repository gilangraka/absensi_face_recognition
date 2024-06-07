import os
import cv2
import urllib.request
import numpy as np
import pandas as pd
from datetime import datetime
import face_recognition
import requests

# Path ke folder gambar dan URL kamera
path = r'C:\Users\roy\Documents\IOT UAS\tubes\image_folder'
url = 'http://192.168.9.247/cam-hi.jpg'  # Pastikan URL ini benar
attendance_dir = os.path.join(os.getcwd(), 'attendance')

# Pastikan direktori attendance ada
os.makedirs(attendance_dir, exist_ok=True)

# Path ke file Attendance.csv
attendance_file = os.path.join(attendance_dir, 'Attendance.csv')

# Buat file Attendance.csv jika belum ada
if not os.path.exists(attendance_file):
    df = pd.DataFrame(columns=["Name", "Time"])
    df.to_csv(attendance_file, index=False)

# Fungsi untuk mencari encoding gambar
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def send_image_to_laravel(name):
    url = "http://192.168.9.147/dashboard-absensi/public/api/set_absen/" + name
    response = requests.get(url)
    if response.status_code == 200:
        print('Berhasil absen')
    else:
        print('Gagal absen')


# Fungsi untuk menandai kehadiran
def markAttendance(name):
    with open(attendance_file, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.write(f'\n{name},{dtString}')

# Baca gambar dari folder dan cari encoding
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

encodeListKnown = findEncodings(images)
print('Encoding Complete')

while True:
    try:
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)

        if img is None:
            print("Failed to retrieve image")
            continue

    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")
        break
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
            send_image_to_laravel(name)

    cv2.imshow('Webcam', img)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
