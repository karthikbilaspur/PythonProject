# Cellular Automaton Simulation Summary

This code simulates a cellular automaton where organisms move, reproduce, and interact with their environment. The simulation consists of:
A grid of size 20x20 where organisms and resources are randomly placed
Organisms with energy levels that determine their behavior
Rules dictionary that defines organism behavior based on energy levels:
Low energy: move left or stay
Medium energy: reproduce or move right
High energy: reproduce or move right
Simulation loop that runs for 100 iterations, updating organism positions and energy levels
Key Features:
Organisms move left or right based on rules
Organisms reproduce when energy levels are high enough
Organisms' energy levels increase over time
Grid is updated and displayed at each iteration
Code Structure:
Organism class defines organism behavior and properties
initialize_grid function sets up the grid and places organisms and resources
simulate function runs the simulation loop and updates the grid.
