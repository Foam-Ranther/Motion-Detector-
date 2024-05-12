import winsound

def alertSound():
    # Define frequency and duration (in milliseconds)
    frequency = 2500  # Adjust as desired (2000-8000 Hz is a common beep range)
    duration = 500  # 1 second

    # Calculate volume percentage as a value between 0 and 1
    volume_pct = 0.25

    # Minimum and maximum volume values for Windows
    MIN_VOLUME = 0
    MAX_VOLUME = 65535

    # Convert volume percentage to a valid Windows volume value
    volume = int(volume_pct * (MAX_VOLUME - MIN_VOLUME)) + MIN_VOLUME

    # Play the beep sound
    winsound.Beep(frequency, duration)

# print("Beep sound played!")
