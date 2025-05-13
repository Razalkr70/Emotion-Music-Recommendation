from googleapiclient.discovery import build
import pandas as pd

# ✅ Replace with your actual YouTube API Key
api_key = "AIzaSyD7ifyRMEaxUCGksm5wBbK0x4Qqe71gr8k"
youtube = build('youtube', 'v3', developerKey=api_key)

# Emotion Mappings
emotion_dict = {
    0: "Angry",
    1: "Disgusted",
    2: "Fearful",
    3: "Happy",
    4: "Neutral",
    5: "Sad",
    6: "Surprised"
}

music_suggestions = {
    0: "Stronger Kanye West",
    1: "Numb Linkin Park",
    2: "Demons Imagine Dragons",
    3: "Happy Pharrell Williams",
    4: "Let It Be Beatles",
    5: "Someone Like You Adele",
    6: "On Top of the World Imagine Dragons"
}

# 🔍 Search for a single YouTube video and return details
def search_youtube(query):
    try:
        response = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=1,
            type="video"
        ).execute()

        video = response["items"][0]
        video_id = video["id"]["videoId"]
        title = video["snippet"]["title"]
        channel = video["snippet"]["channelTitle"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"

        return {
            "Name": title,
            "Album": "YouTube Video",
            "Artist": channel,
            "song_url": url,
            "thumbnail_url": thumbnail_url
        }

    except Exception as e:
        print(f"Error fetching from YouTube for '{query}': {e}")
        return {
            "Name": query,
            "Album": "Unknown",
            "Artist": "Unknown",
            "song_url": "MISSING_URL",
            "thumbnail_url": ""
        }

# 🎵 Recommend music based on detected emotion
def music_rec(emotion_id=3):
    query = music_suggestions.get(emotion_id, "chill music")
    print(f"🎵 Searching YouTube for emotion {emotion_dict.get(emotion_id, 'Unknown')} ➝ {query}")

    try:
        response = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=10,  # ⬅️ Show 10 songs now
            type="video"
        ).execute()

        results = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"

            results.append({
                "Name": title,
                "Album": "YouTube Video",
                "Artist": channel,
                "song_url": url,
                "thumbnail_url": thumbnail_url
            })

        return results

    except Exception as e:
        print(f"❌ Error fetching from YouTube: {e}")
        return []

# 📝 Optional: Save a single search result to CSV
def fetch_and_save_playlist_data(emotion, song_name, filename):
    track = search_youtube(song_name)
    print(f"Fetched: {track['Name']} by {track['Artist']}")

    df = pd.DataFrame([track])
    df.to_csv(f'songs/{filename}.csv', index=False)
    print(f"✅ CSV for '{emotion}' saved as songs/{filename}.csv")

# 🏁 Run for generating CSVs if needed
if __name__ == "__main__":
    for emotion, song_name in music_suggestions.items():
        filename = emotion_dict[emotion].lower()
        fetch_and_save_playlist_data(emotion_dict[emotion], song_name, filename)
