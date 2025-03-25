# Maze Explorer

![Maze Explorer Game](https://via.placeholder.com/800x400?text=Maze+Explorer+Game)

## Overview

Maze Explorer is an engaging terminal-based maze game where players navigate through procedurally generated mazes, collect keys and coins, and avoid traps to reach the exit. The game features colorful ASCII graphics, multiple difficulty levels, and an intelligent hint system to help when you're stuck.

## Features

- **Procedurally Generated Mazes**: Each game creates a unique maze using a randomized depth-first search algorithm
- **Colorful Terminal Interface**: Enjoy vibrant colored elements that bring the maze to life
- **Multiple Game Elements**:
  - **Keys (K)**: Collect all required keys to unlock the exit
  - **Coins (C)**: Gather coins for extra points
  - **Traps (T)**: Avoid these or your game ends
  - **Exit (E)**: Your destination, but you need keys to escape!
- **Difficulty Levels**: Choose between Easy, Medium, and Hard modes
- **Customizable Maze Size**: Adjust width and height to your preference
- **Intelligent Hint System**: Stuck? Use the hint feature to see the next best move
- **Full Game UI**: Complete with menus, settings, and instructions

## Installation

### Prerequisites

- Python 3.6 or higher
- Keyboard library

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/maze-explorer.git
   cd maze-explorer
   ```

2. Install required dependencies:
   ```
   pip install keyboard
   ```

3. Run the game:
   ```
   python maze_game.py
   ```

## How to Play

### Controls

- **Arrow Keys**: Move your character (P) through the maze
- **H**: Show a hint (reveals the next step on the optimal path)
- **R**: Restart the game with a new maze
- **Q**: Quit the game

### Objective

1. Navigate through the maze to find the exit (E)
2. Collect all required keys (K) to unlock the exit
3. Gather coins (C) for a higher score
4. Avoid traps (T) that will end your game
5. Reach the exit with all required keys to win!

### Game Elements

| Symbol | Description |
|--------|-------------|
| P | Player (that's you!) |
| E | Exit (your destination) |
| K | Key (collect to unlock the exit) |
| C | Coin (collect for points) |
| T | Trap (avoid these!) |
| # | Wall (you can't move through these) |

## Customization

From the Settings menu, you can:

- Change difficulty level (Easy, Medium, Hard)
- Adjust maze width (10-50)
- Adjust maze height (10-30)

Each difficulty level changes:
- Number of required keys
- Number of traps
- Number of coins

## Technical Details

The game implements several interesting algorithms and techniques:

- **Maze Generation**: Uses randomized depth-first search (recursive backtracking)
- **Pathfinding**: Implements breadth-first search (BFS) for the hint system
- **Terminal Coloring**: Uses ANSI escape codes for colorful display
- **Event Handling**: Keyboard event handling for responsive controls

## Code Structure

- **MazeGame Class**: Main class that handles game logic
  - `generate_maze()`: Creates a random maze using DFS
  - `move_player()`: Handles player movement and interactions
  - `solve_maze()`: Finds the shortest path to exit using BFS
  - `print_maze()`: Renders the maze with colors
  - `show_hint()`: Displays the next best move
  - UI methods for menus and settings

## Known Issues

- Some terminal emulators may not display colors correctly
- Game requires a terminal with at least 30 rows and 80 columns for optimal display
- Keyboard library may require administrator privileges on some systems

## Future Enhancements

- [ ] Save/load game functionality
- [ ] High score system
- [ ] More maze generation algorithms
- [ ] Additional game elements like teleporters
- [ ] Sound effects (terminal bell)
- [ ] More advanced enemy AI

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by classic maze games
- Thanks to the keyboard library developers
- Special thanks to all contributors and testers

---

Enjoy exploring the maze! For issues or suggestions, please open an issue on GitHub.
