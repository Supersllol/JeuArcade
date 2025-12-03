import pygame
import json

pygame.init()
file = "Semi-Charmed Life"

pygame.mixer.music.load(f"{file}.wav")
ecran = pygame.display.set_mode((400, 50))
LANCEMENT = True

# ------------------------------
# Load JSON and choose section
# ------------------------------
with open(f"beat-{file}.json", "r", encoding="utf8") as f:
    data = json.load(f)

SECTION = "1"  # <-- change this to "2", "3", etc.
notes_raw = data.get(SECTION, [])

# Convert note objects to a list of timestamps (in seconds)
notes = [note["time"] for note in notes_raw]

# Start music
print(notes[0] * 1000)
pygame.mixer.music.play(start=notes[0])
start = pygame.time.get_ticks()

# ------------------------------
# Main Loop
# ------------------------------
while LANCEMENT:
    ecran.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            LANCEMENT = False

    elapsed = pygame.time.get_ticks() - start

    # Only process if we still have notes
    if notes:
        currentBeat = notes[0] * 1000  # convert sec → ms

        print(currentBeat, elapsed)

        # If within hit window
        if abs(elapsed - currentBeat) < 10:
            pygame.draw.circle(ecran, "red", (200, 25), 15)

        # If note time has passed, remove it
        elif elapsed > currentBeat:
            notes.pop(0)
    else:
        pygame.mixer.music.stop()

    pygame.display.update()

pygame.quit()
