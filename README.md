# Real-Time Emotion-Based Music Recommendation System

A real-time emotion detection system that analyzes facial expressions through a camera feed and recommends songs based on the detected emotion. This system uses **facial emotion recognition** and integrates with music APIs to provide personalized music recommendations suited to the user's emotional state.

## 📌 Overview

This project leverages **OpenCV** and **Convolutional Neural Networks (CNN)** for real-time facial emotion recognition from a camera feed. Based on the detected emotion, the system fetches music recommendations from an external music API like **YouTube Data API** or **Spotify API**, offering personalized playlists for the user's mood. The system can detect emotions such as **Happy**, **Sad**, **Angry**, **Surprised**, and **Neutral**, and recommend music accordingly.

## 🧠 Features

- **Real-Time Emotion Detection** using a webcam feed.
- **Emotion Classification** into categories such as **Happy**, **Sad**, **Angry**, **Surprised**, **Neutral**.
- **Music Recommendation** based on the detected emotion (e.g., happy music for happy emotions, calm music for sad emotions).
- Integration with **YouTube Data API** (or **Spotify API**) for fetching songs and playlists.
- Display of emotion on the webcam feed in real-time.
- Audio or video playback of recommended songs.

## 🛠️ Tech Stack

- **Python**
- **OpenCV** for real-time facial emotion detection
- **Keras / TensorFlow** for emotion classification (using CNN models)
- **Music APIs** (YouTube Data API, Spotify API, or similar)
- **NumPy** for numerical operations
- **Matplotlib** for visualizations (optional)
- **Flask** (if integrating into a web interface)

## 🚀 How to Run

1. **Clone the repository:**
  
   git clone https://github.com/razalkr70/Emotion-Based-Music-Recommendation.git
   cd Emotion-Based-Music-Recommendation

2. **Install dependencies:**

3. **Set up API keys for YouTube Data API or Spotify API:**
4. **Run the App**



## 💡 Use Cases

- **Personalized music recommendations** for emotional well-being.
- **Interactive apps** where users can listen to music that matches their emotional state.
- **Mental health applications** where music is used as a therapeutic tool based on the user's current mood.
- **Event management**, offering music based on crowd emotions in real-time.

## 🎯 Advantages

- **Personalized Music Experience**: Users receive music recommendations tailored to their emotional state, enhancing their listening experience and providing a sense of emotional connection.
- **Mood-Boosting**: The system can recommend uplifting music for users feeling down, or calming music for those experiencing stress or anxiety, potentially improving mental well-being.
- **Real-Time Interaction**: The emotion detection and music recommendation process happens in real-time, allowing for immediate feedback and engagement.
- **Wide Application Scope**: The system can be used in various domains, such as mental health apps, personalized entertainment apps, event management (to match crowd mood), and interactive installations.
- **Emotion Awareness**: Helps raise awareness of emotions, allowing users to reflect on their emotional state through the medium of music.

