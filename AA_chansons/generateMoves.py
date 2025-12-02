import librosa
import numpy as np
import random
import json

name = "Semi-Charmed Life"
y, sr = librosa.load(f"{name}.wav")

# Detect beats
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')

# Remove duplicates and sort
timestamps = sorted(set(list(beats)))

# Prepare JSON structure
data = {"sections": {}, "notes": []}

for i in range(4):
    data["sections"][i] = {"start": 0}

# Fill note list
for t in timestamps:
    data["notes"].append({
        "time": float(f"{t:.3f}"),  # store time as float
        "move": random.choice([0, 1, 2, 3])
    })

# Write JSON file
with open(f"beat-{name}.json", "w", encoding="utf8") as f:
    json.dump(data, f, indent=4)
