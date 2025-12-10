import librosa
import numpy as np
import random
import json
import pygame

name = "Take on Me"
y, sr = librosa.load(f"{name}.mp3")

# Detect beats
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')

# Remove duplicates and sort
timestamps = sorted(set(list(beats)))

# Prepare JSON structure
data = {
    "Title": name,
    "Artist": "",
    "BPM": None,
    "songLength": None,
    "numNotes": len(timestamps),
    "sections": {},
    "notes": []
}
pygame.init()
songLength = pygame.mixer.Sound(f"{name}.mp3").get_length()
data["songLength"] = songLength
data["BPM"] = int(round(len(timestamps) / (songLength / 60)))

for i in range(6):
    quartile = songLength / 6
    data["sections"][i] = {"start": (i) * quartile}

# Fill note list
for t in timestamps:
    data["notes"].append({
        "time": float(f"{t:.3f}"),  # store time as float
        "move": random.choice([0, 1, 2, 3])
    })

# Write JSON file
with open(f"beat-{name}.json", "w", encoding="utf8") as f:
    json.dump(data, f, indent=4)
