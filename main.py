import random
import os
import time
import keyboard
import math
from collections import deque

class MazeGame:
    # Terminal colors
    COLORS = {
        'RESET': '\033[0m',
        'BLACK': '\033[30m',
        'RED': '\033[31m',
        'GREEN': '\033[32m',
        'YELLOW': '\033[33m',
        'BLUE': '\033[34m',
        'MAGENTA': '\033[35m',
        'CYAN': '\033[36m',
        'WHITE': '\033[37m',
        'BOLD': '\033[1m',
        'BG_BLACK': '\033[40m',
        'BG_RED': '\033[41m',
        'BG_GREEN': '\033[42m',
        'BG_YELLOW': '\033[43m',
        'BG_BLUE': '\033[44m',
        'BG_MAGENTA': '\033[45m',
        'BG_CYAN': '\033[46m',
        'BG_WHITE': '\033[47m',
    }

    # Maze elements
    WALL = '#'
    PATH = ' '
    PLAYER = 'P'
    EXIT = 'E'
    KEY = 'K'
    TRAP = 'T'
    COIN = 'C'

    def __init__(self, width=25, height=15):
        self.width = width
        self.height = height
        self.maze = None
        self.player_pos = None
        self.exit_pos = None
        self.keys = []
        self.traps = []
        self.coins = []
        self.keys_collected = 0
        self.required_keys = 0
        self.coins_collected = 0
        self.moves = 0
        self.game_over = False
        self.win = False
        self.start_time = None
        self.difficulty = 'medium'
        self.generate_maze()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_colored(self, text, color=None, bg_color=None, bold=False):
        """Print text with specified colors."""
        color_code = self.COLORS.get(color.upper(), '') if color else ''
        bg_code = self.COLORS.get(f'BG_{bg_color.upper()}', '') if bg_color else ''
        bold_code = self.COLORS['BOLD'] if bold else ''
        reset = self.COLORS['RESET']
        print(f"{color_code}{bg_code}{bold_code}{text}{reset}", end='')

    def generate_maze(self):
        """Generate a random maze using a randomized depth-first search algorithm."""
        # Initialize maze with walls
        self.maze = [[self.WALL for _ in range(self.width)] for _ in range(self.height)]
        
        # Starting position (always odd coordinates to ensure paths are separated by walls)
        start_y, start_x = 1, 1
        self.maze[start_y][start_x] = self.PATH
        
        # Stack for backtracking
        stack = [(start_y, start_x)]
        
        # Directions: up, right, down, left
        directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        
        # Generate the maze paths
        while stack:
            current_y, current_x = stack[-1]
            
            # Randomize directions
            random.shuffle(directions)
            
            # Flag to check if we can move in any direction
            moved = False
            
            for dy, dx in directions:
                new_y, new_x = current_y + dy, current_x + dx
                
                # Check if the new position is within bounds and is a wall
                if (0 < new_y < self.height - 1 and 0 < new_x < self.width - 1 and 
                    self.maze[new_y][new_x] == self.WALL):
                    
                    # Carve a path by making the wall between current and new position a path
                    self.maze[current_y + dy // 2][current_x + dx // 2] = self.PATH
                    self.maze[new_y][new_x] = self.PATH
                    
                    # Add the new position to the stack
                    stack.append((new_y, new_x))
                    moved = True
                    break
            
            # If we couldn't move in any direction, backtrack
            if not moved:
                stack.pop()
        
        # Place player at the start
        self.player_pos = (start_y, start_x)
        
        # Place exit at a random position far from the player
        possible_exits = [(y, x) for y in range(1, self.height - 1) for x in range(1, self.width - 1) 
                         if self.maze[y][x] == self.PATH and abs(y - start_y) + abs(x - start_x) > (self.width + self.height) // 3]
        
        if possible_exits:
            self.exit_pos = random.choice(possible_exits)
        else:
            # Fallback if no suitable exit found
            far_positions = [(y, x) for y in range(1, self.height - 1) for x in range(1, self.width - 1) 
                           if self.maze[y][x] == self.PATH and (y != start_y or x != start_x)]
            self.exit_pos = random.choice(far_positions) if far_positions else (self.height - 2, self.width - 2)
        
        # Set difficulty-based parameters
        self.set_difficulty()
        
        # Place keys, traps, and coins
        self.place_items()
        
        # Mark the exit
        y, x = self.exit_pos
        self.maze[y][x] = self.EXIT

    def set_difficulty(self):
        """Set game parameters based on difficulty level."""
        if self.difficulty == 'easy':
            self.required_keys = max(1, (self.width + self.height) // 25)
            trap_count = max(2, (self.width + self.height) // 15)
            coin_count = max(5, (self.width + self.height) // 8)
        elif self.difficulty == 'medium':
            self.required_keys = max(2, (self.width + self.height) // 20)
            trap_count = max(3, (self.width + self.height) // 12)
            coin_count = max(7, (self.width + self.height) // 7)
# Added comment
        else:  # hard
            self.required_keys = max(3, (self.width + self.height) // 15)
            trap_count = max(5, (self.width + self.height) // 10)
            coin_count = max(10, (self.width + self.height) // 6)
        
        # Prepare lists for items
        self.keys = []
        self.traps = []
        self.coins = []
        
        # Determine counts
        self.keys_to_place = self.required_keys
        self.traps_to_place = trap_count
        self.coins_to_place = coin_count

    def place_items(self):
        """Place keys, traps and coins in the maze."""
        available_positions = [(y, x) for y in range(1, self.height - 1) for x in range(1, self.width - 1) 
                             if self.maze[y][x] == self.PATH and (y, x) != self.player_pos and (y, x) != self.exit_pos]
        
        # Shuffle positions for random placement
        random.shuffle(available_positions)
        
        # Place keys
        for i in range(min(self.keys_to_place, len(available_positions))):
            y, x = available_positions[i]
            self.keys.append((y, x))
            self.maze[y][x] = self.KEY
        
        # Place traps (avoid placing on keys)
        trap_positions = available_positions[self.keys_to_place:self.keys_to_place + self.traps_to_place]
        for y, x in trap_positions:
# Added comment
            self.traps.append((y, x))
            self.maze[y][x] = self.TRAP
        
        # Place coins (avoid placing on keys and traps)
        coin_positions = available_positions[self.keys_to_place + self.traps_to_place:
                                          self.keys_to_place + self.traps_to_place + self.coins_to_place]
        for y, x in coin_positions:
            self.coins.append((y, x))
            self.maze[y][x] = self.COIN

    def print_maze(self):
        """Display the maze with colors."""
        self.clear_screen()
        
        # Print header
        print("\n" + "=" * (self.width * 2 + 5))
        self.print_colored("  MAZE EXPLORER  ", "black", "green", True)
        print("\n" + "=" * (self.width * 2 + 5))
        
        # Print game info
        print(f"Keys: {self.keys_collected}/{self.required_keys} | Coins: {self.coins_collected} | Moves: {self.moves}")
        print("-" * (self.width * 2 + 5))
        
        # Print the maze
        for y in range(self.height):
            print(" ", end='')
            for x in range(self.width):
                if (y, x) == self.player_pos:
                    self.print_colored(self.PLAYER, "yellow", "blue", True)
                    print(" ", end='')
                elif self.maze[y][x] == self.WALL:
                    self.print_colored(self.WALL, "white", "black")
                    print(" ", end='')
                elif self.maze[y][x] == self.EXIT:
                    self.print_colored(self.EXIT, "black", "green")
                    print(" ", end='')
                elif self.maze[y][x] == self.KEY:
                    self.print_colored(self.KEY, "yellow")
                    print(" ", end='')
                elif self.maze[y][x] == self.TRAP:
                    self.print_colored(self.TRAP, "red")
                    print(" ", end='')
                elif self.maze[y][x] == self.COIN:
                    self.print_colored(self.COIN, "cyan")
                    print(" ", end='')
                else:
                    print(self.maze[y][x] + " ", end='')
            print()
        
        # Print footer with controls
        print("-" * (self.width * 2 + 5))
        print("Controls: Arrow Keys to move, Q to quit, R to restart")
        
        # Print messages based on game state
        if self.game_over:
            if self.win:
                self.print_colored("\nCongratulations! You escaped the maze!", "green", bold=True)
                elapsed_time = time.time() - self.start_time
                print(f"\nTime: {elapsed_time:.2f} seconds | Moves: {self.moves} | Coins: {self.coins_collected}")
            else:
                self.print_colored("\nGame Over! You stepped on a trap!", "red", bold=True)
            print("\nPress 'R' to play again or 'Q' to quit.")

    def move_player(self, direction):
        """Move player in the specified direction."""
        if self.game_over:
            return
        
        dy, dx = 0, 0
        if direction == 'up':
            dy = -1
        elif direction == 'down':
            dy = 1
        elif direction == 'left':
            dx = -1
        elif direction == 'right':
            dx = 1
        
        new_y, new_x = self.player_pos[0] + dy, self.player_pos[1] + dx
        
        # Check if the move is valid
        if 0 <= new_y < self.height and 0 <= new_x < self.width and self.maze[new_y][new_x] != self.WALL:
            # Update current position
            y, x = self.player_pos
            self.maze[y][x] = self.PATH
            
            # Update player position
            self.player_pos = (new_y, new_x)
            
            # Check what's at the new position
            if self.maze[new_y][new_x] == self.KEY:
                self.keys_collected += 1
                self.keys.remove((new_y, new_x))
            elif self.maze[new_y][new_x] == self.TRAP:
                self.game_over = True
                self.win = False
            elif self.maze[new_y][new_x] == self.COIN:
                self.coins_collected += 1
                self.coins.remove((new_y, new_x))
            elif self.maze[new_y][new_x] == self.EXIT:
                if self.keys_collected >= self.required_keys:
                    self.game_over = True
                    self.win = True
            
            # Mark new position with player symbol (except if game over)
            if not self.game_over:
                self.maze[new_y][new_x] = self.PLAYER
            
            self.moves += 1

    def solve_maze(self):
        """Find the shortest path from player to exit using BFS."""
# Added comment
        start = self.player_pos
        end = self.exit_pos
        
        # Directions: up, right, down, left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # Initialize queue with starting position
        queue = deque([start])
        
        # Keep track of visited cells and their parent cell
        visited = {start: None}
        
        while queue:
            current = queue.popleft()
            
            # If we reached the exit, we're done
            if current == end:
                break
            
            # Try all directions
            for dy, dx in directions:
                new_y, new_x = current[0] + dy, current[1] + dx
                
                # Check if the move is valid and cell hasn't been visited
                if (0 <= new_y < self.height and 0 <= new_x < self.width and 
                    self.maze[new_y][new_x] != self.WALL and (new_y, new_x) not in visited):
                    
                    visited[(new_y, new_x)] = current
                    queue.append((new_y, new_x))
        
        # If exit wasn't reached, return None
        if end not in visited:
            return None
        
        # Reconstruct the path
        path = []
        current = end
        while current != start:
            path.append(current)
            current = visited[current]
        
        # Reverse to get path from start to end
        path.reverse()
        return path

    def show_hint(self):
# Added comment
        """Show the next step in the shortest path to the exit."""
        path = self.solve_maze()
        if not path:
            print("No path to exit found!")
            return
        
        # Mark the next step with a special marker for a short time
        if path:
            next_step = path[0]
            original = self.maze[next_step[0]][next_step[1]]
            self.maze[next_step[0]][next_step[1]] = 'H'
            self.print_maze()
            time.sleep(1)
            self.maze[next_step[0]][next_step[1]] = original
            self.print_maze()

    def start_game(self):
        """Main game loop."""
        self.start_time = time.time()
        self.game_over = False
        self.win = False
        self.keys_collected = 0
        self.coins_collected = 0
        self.moves = 0
        
        # Show the initial state
        self.print_maze()
        
        # Set up keyboard event handlers
        keyboard.on_press_key("up", lambda _: self.handle_key("up"))
        keyboard.on_press_key("down", lambda _: self.handle_key("down"))
        keyboard.on_press_key("left", lambda _: self.handle_key("left"))
        keyboard.on_press_key("right", lambda _: self.handle_key("right"))
        keyboard.on_press_key("q", lambda _: self.handle_key("quit"))
        keyboard.on_press_key("r", lambda _: self.handle_key("restart"))
# Added comment
        keyboard.on_press_key("h", lambda _: self.handle_key("hint"))
        
        try:
            # Keep the program running until user quits
            while True:
                time.sleep(0.1)  # To prevent CPU hogging
        except KeyboardInterrupt:
            pass
        finally:
            # Clean up keyboard handlers
            keyboard.unhook_all()

    def handle_key(self, key):
        """Handle keyboard input."""
        if key == "quit":
            keyboard.unhook_all()
            exit(0)
        elif key == "restart":
            self.generate_maze()
            self.start_time = time.time()
            self.game_over = False
            self.win = False
            self.keys_collected = 0
            self.coins_collected = 0
            self.moves = 0
        elif key == "hint":
            self.show_hint()
        elif not self.game_over:
            self.move_player(key)
            self.print_maze()

# Added comment
    def show_main_menu(self):
        """Display the main menu."""
        while True:
            self.clear_screen()
            print("\n" + "=" * 40)
            self.print_colored("  MAZE EXPLORER  ", "black", "green", True)
            print("\n" + "=" * 40)
            print("\n1. Start Game")
            print("2. Settings")
            print("3. Instructions")
            print("4. Quit")
            print("\nEnter your choice (1-4): ", end="")
            
            choice = input().strip()
            
            if choice == '1':
                return self.start_game()
            elif choice == '2':
                self.show_settings()
            elif choice == '3':
                self.show_instructions()
            elif choice == '4':
                print("Thanks for playing!")
                exit(0)
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)

    def show_settings(self):
        """Display and modify game settings."""
        while True:
            self.clear_screen()
            print("\n" + "=" * 40)
            self.print_colored("  SETTINGS  ", "black", "cyan", True)
            print("\n" + "=" * 40)
            print(f"\n1. Difficulty: {self.difficulty}")
            print(f"2. Maze Width: {self.width}")
            print(f"3. Maze Height: {self.height}")
            print("4. Back to Main Menu")
            print("\nEnter your choice (1-4): ", end="")
            
            choice = input().strip()
            
            if choice == '1':
                print("\nSelect difficulty:")
                print("1. Easy")
                print("2. Medium")
                print("3. Hard")
                diff_choice = input("Enter choice (1-3): ").strip()
                if diff_choice == '1':
                    self.difficulty = 'easy'
# Added comment
                elif diff_choice == '2':
                    self.difficulty = 'medium'
                elif diff_choice == '3':
                    self.difficulty = 'hard'
            elif choice == '2':
                try:
                    new_width = int(input("\nEnter new width (10-50): ").strip())
                    if 10 <= new_width <= 50:
                        self.width = new_width
                    else:
                        print("Width must be between 10 and 50.")
                        time.sleep(1)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    time.sleep(1)
            elif choice == '3':
                try:
                    new_height = int(input("\nEnter new height (10-30): ").strip())
                    if 10 <= new_height <= 30:
                        self.height = new_height
                    else:
                        print("Height must be between 10 and 30.")
                        time.sleep(1)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    time.sleep(1)
            elif choice == '4':
                # Regenerate maze with new settings
                self.generate_maze()
                return
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)

    def show_instructions(self):
        """Display game instructions."""
        self.clear_screen()
        print("\n" + "=" * 40)
        self.print_colored("  INSTRUCTIONS  ", "black", "yellow", True)
        print("\n" + "=" * 40)
        print("\nWelcome to Maze Explorer!")
        print("\nObjective:")
        print("- Navigate through the maze to find the exit (E)")
        print("- Collect all required keys (K) to unlock the exit")
        print("- Collect coins (C) for extra points")
        print("- Avoid traps (T) that will end your game")
        
        print("\nControls:")
        print("- Use arrow keys to move")
        print("- Press 'H' for a hint (shows next step)")
        print("- Press 'R' to restart the game")
        print("- Press 'Q' to quit")
        
        print("\nSymbols:")
        print("- P: Player (that's you!)")
        print("- E: Exit")
        print("- K: Key (collect to unlock the exit)")
        print("- C: Coin (collect for points)")
        print("- T: Trap (avoid these!)")
        print("- #: Wall (you can't move through these)")
        
        print("\nPress any key to return to the main menu...", end="")
        input()

# Start the game when run directly
if __name__ == "__main__":
    game = MazeGame()
    game.show_main_menu()