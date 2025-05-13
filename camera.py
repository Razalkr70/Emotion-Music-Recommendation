import numpy as np
import cv2
from PIL import Image
import pandas as pd
import datetime
from threading import Thread, Lock
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Load Pretrained Emotion Recognition Model
emotion_model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(1024, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])
emotion_model.load_weights('model.h5')

cv2.ocl.setUseOpenCL(False)

# Emotion Dictionary
emotion_dict = {
    0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy",
    4: "Neutral", 5: "Sad", 6: "Surprised"
}

# Music Recommendation Files
music_dist = {
    0: "songs/angry.csv", 1: "songs/disgusted.csv", 2: "songs/fearful.csv",
    3: "songs/happy.csv", 4: "songs/neutral.csv", 5: "songs/sad.csv", 6: "songs/surprised.csv"
}


# Thread-safe Emotion State
class EmotionState:
    _emotion_id = 3  # Default = Happy
    _lock = Lock()

    @classmethod
    def set(cls, val):
        with cls._lock:
            cls._emotion_id = val

    @classmethod
    def get(cls):
        with cls._lock:
            return cls._emotion_id


# Webcam video capture in separate thread
class WebcamVideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True


# Main class for video + emotion + music
class VideoCamera:
    def __init__(self):
        self.cap = WebcamVideoStream(src=0).start()

    def get_frame(self):
        image = self.cap.read()
        image = cv2.resize(image, (600, 500))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in face_rects:
            cv2.rectangle(image, (x, y - 50), (x + w, y + h + 10), (0, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)

            prediction = emotion_model.predict(cropped_img, verbose=0)
            maxindex = int(np.argmax(prediction))
            EmotionState.set(maxindex)

            cv2.putText(image, emotion_dict[maxindex], (x + 20, y - 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Fix bluish tint by keeping image in BGR (no RGB/PIL conversion)
        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes(), get_music_recommendation()

    @staticmethod
    def get_emotion():
        return EmotionState.get()


# Music Recommendation Logic
# Updated music recommendation logic (includes YouTube URL & Thumbnail)
def get_music_recommendation():
    emotion_id = EmotionState.get()
    try:
        df = pd.read_csv(music_dist.get(emotion_id, "songs/neutral.csv"))

        # Make sure required columns exist
        expected_cols = {'Name', 'Album', 'Artist', 'song_url', 'thumbnail_url'}
        if not expected_cols.issubset(df.columns):
            raise ValueError("CSV file is missing expected columns.")

        # Randomize and return 10 or fewer recommendations
        df = df.sample(n=min(20, len(df)))

        return df[['Name', 'Album', 'Artist', 'song_url', 'thumbnail_url']].to_dict(orient='records')
    except Exception as e:
        print(f"[ERROR] Music load failed: {e}")
        return []

