from flask import Flask
from flask import jsonify
import requests
import cv2
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/create_user/<nama_file>")
def download_file(nama_file):
    url = "http://192.168.110.1/dashboard-absensi/storage/app/public/uploads/" + nama_file
    save_path = "downloaded_file/" + nama_file
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(save_path, 'wb') as file :
            file.write(response.content)
        
        # Memecah video menjadi frame frame
        output_folder = "data_mhs/" + nama_file.split(".")[0]
        os.makedirs(output_folder)
        cap = cv2.VideoCapture("downloaded_file/" + nama_file)
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
        cap.release()

        return jsonify({
            "message": "Sukses mendownload data"
        })
    else:
        return jsonify({
            "message" : "Gagal mendownload data"
        })
    
@app.route("/validation_image/<nama_image>")
def validasi_img(nama_image) :

    # Get image untuk di validasi
    image = "http://192.168.110.1/dashboard-absensi/storage/app/public/validation/" + nama_image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
