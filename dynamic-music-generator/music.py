import os
from typing import Any, cast

import magenta.music as mm
import pretty_midi
import pygame
import numpy as np

# pyright: reportMissingImports=false
try:
    from tensorflow.keras.models import Sequential  # type: ignore[import-not-found]
    from tensorflow.keras.layers import Dense, Dropout, LSTM  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - optional dependency during static analysis
    Sequential = cast(Any, None)
    Dense = cast(Any, None)
    Dropout = cast(Any, None)
    LSTM = cast(Any, None)

# Define a function to generate music
def generate_music(length: int) -> None:
    # Create a note sequence
    # magenta.music doesn't always provide usable type information for static checkers
    sequence: Any = getattr(mm, "NoteSequence")()

    # Define the notes and durations
    notes: list[int] = [60, 62, 64, 65, 67, 69, 71, 72]
    durations: list[float] = [0.5, 0.5, 1, 1, 0.5, 0.5, 1, 1]

    # Generate the music
    start_time = 0.0
    for _ in range(length):
        note = int(np.random.choice(notes))
        duration = float(np.random.choice(durations))
        sequence.notes.add(
            pitch=note,
            start_time=start_time,
            end_time=start_time + duration,
            velocity=80,
        )
        start_time += duration

    # Save the music to a MIDI file
    getattr(mm, "sequence_proto_to_midi_file")(sequence, "ai_music.mid")

# Define a function to play the music
def play_music(file: str) -> None:
    pygame.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# Define a function to train an LSTM model
def train_lstm_model() -> Any:
    # Define the model architecture
    model = cast(Any, Sequential())
    model.add(LSTM(64, input_shape=(None, 1)))
    model.add(Dropout(0.2))
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer="adam", loss="mean_squared_error")

    # Train the model
    # You'll need to provide your own dataset of music
    # For this example, we'll use a random dataset
    X_train: Any = np.random.rand(100, 10, 1)
    y_train: Any = np.random.rand(100, 1)
    model.fit(X_train, y_train, epochs=100)

    return model

# Define a function to generate music using an LSTM model
def generate_music_lstm(model: Any, length: int) -> list[float]:
    # Create a starting sequence
    sequence: Any = np.random.rand(1, 1, 1)

    # Generate the music
    music: list[float] = []
    for _ in range(length):
        prediction: Any = model.predict(sequence)
        note_value = float(prediction[0][0])
        music.append(note_value)
        sequence = np.roll(sequence, -1)
        sequence[0][-1][0] = note_value

    return music

# Generate music
generate_music(100)

# Play the music
play_music("ai_music.mid")

# Train an LSTM model
model = train_lstm_model()

# Generate music using the LSTM model
music = generate_music_lstm(model, 100)
print(music)