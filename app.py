from flask import Flask, render_template, Response, request, redirect, url_for, session, jsonify
import os
from camera import VideoCamera
from Spotipywe import music_rec  # Your YouTube-based recommendation function

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")  # Default for local dev

# Dummy credentials
USER_CREDENTIALS = {"user": "user123"}

# Updated headings including Thumbnail and Link
headings = ("Thumbnail", "Title", "Artist", "Album", "YouTube Link")

# -------- AUTH ROUTES -------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="❌ Invalid username or password")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# -------- MAIN PAGE -------- #
@app.route('/index')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', headings=headings)

# -------- VIDEO STREAM ROUTE -------- #
def gen(camera):
    while True:
        frame, _ = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    if 'user' not in session:
        return redirect(url_for('login'))
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# -------- API: Music Recommendation -------- #
@app.route('/recommend/<int:emotion>')
def recommend(emotion):
    print(f"🎯 Emotion detected: {emotion}")
    songs = music_rec(emotion)
    if not songs:
        return jsonify({"error": "No songs found"}), 404
    return jsonify(songs)

@app.route('/t', methods=["GET"])
def test_recommendation():
    data = music_rec()
    print("\n=== DEBUG /t RESPONSE ===")
    for song in data:
        print(song)
    return jsonify(data)

@app.route('/current_emotion')
def current_emotion():
    emotion_id = VideoCamera.get_emotion()
    return jsonify({'emotion': emotion_id})

# -------- RUN APP -------- #
if __name__ == '__main__':
    app.run(debug=True)
