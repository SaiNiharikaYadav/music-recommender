import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np

# Spotify credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get album cover
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        return results["tracks"]["items"][0]["album"]["images"][0]["url"]
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # default image

# Load and clean the data
df = pd.read_csv("spotify_millsongdata.csv")
df.dropna(subset=["text", "song", "artist"], inplace=True)
df.drop_duplicates(subset="song", inplace=True)
df = df.sample(1000, random_state=42).reset_index(drop=True)  # limit to 1000 songs for demo

# Dummy similarity matrix (safe size)
similarity = np.random.rand(len(df), len(df))

# Recommendation function
def recommend(song):
    if song not in df['song'].values:
        return [], []
    index = df[df['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_names = []
    recommended_posters = []
    for i in distances:
        rec_song = df.iloc[i[0]]["song"]
        rec_artist = df.iloc[i[0]]["artist"]
        recommended_names.append(rec_song)
        recommended_posters.append(get_song_album_cover_url(rec_song, rec_artist))
    return recommended_names, recommended_posters

# Streamlit UI
st.title("🎵 Music Recommender System")
song_list = df["song"].values
selected_song = st.selectbox("🎶 Type or select a song:", song_list)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_song)
    if names:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
    else:
        st.warning("No recommendations found.")
