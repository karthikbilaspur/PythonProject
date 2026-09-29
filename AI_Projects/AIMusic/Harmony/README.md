
Harmony Generation Project
Overview
This project generates harmonies for a given melody based on a specified musical style. The code uses a simple algorithm to generate harmonies based on intervals defined for each musical style.
Features
Musical Style Support: The code supports multiple musical styles, including classical, jazz, and pop.
Interval-Based Harmony Generation: The code generates harmonies based on intervals defined for each musical style.
Flexible Melody and Chord Progression Input: The code allows users to input their own melody and chord progression.
Usage
Define the Melody: Define the melody as a list of notes (e.g., ['C', 'D', 'E', 'G', 'A', 'G', 'F', 'E', 'D', 'C', 'G', 'A', 'B', 'A', 'G', 'F']).
Define the Chord Progression: Define the chord progression as a list of chords (e.g., ['C', 'G', 'Am', 'F']).
Specify the Musical Style: Specify the musical style (e.g., 'classical', 'jazz', or 'pop').
Run the Code: Run the code to generate harmonies for the specified melody and musical style.
Code Structure
The code consists of two main functions:
generate_harmonies: This function generates harmonies for a given melody and musical style.
get_harmony_note: This function calculates the harmony note based on the interval and note.
Example Output
The code will output the generated harmonies for each note in the melody, along with the corresponding melody note.
Code
Melody Note: C, Harmony Notes: ['E', 'G']
Melody Note: D, Harmony Notes: ['F#', 'A']
Melody Note: E, Harmony Notes: ['G#', 'B']
...
Future Development
Add More Musical Styles: Add more musical styles and intervals to the code.
Improve Harmony Generation Algorithm: Improve the harmony generation algorithm to produce more complex and interesting harmonies.
Integrate with Music Generation Tools: Integrate the code with music generation tools to produce complete musical compositions.