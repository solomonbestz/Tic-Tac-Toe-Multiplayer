# Tic Tac Toe Multiplayer with Socket

## Overview
This project enhances the classic Tic Tac Toe game with multiplayer functionality using Python sockets. Players can now compete against each other over a network connection.

## Features
- Classic 3x3 Tic Tac Toe gameplay
- Network multiplayer functionality
- Turn-based system with clear visual indicators
- Win detection for all possible combinations
- Clean Pygame interface

## Requirements
- Python 3.6+
- Pygame
- Basic network connectivity between players

## Installation
1. Clone the repository:
   ```bash git clone https://github.com/solomonbestz/Tic-Tac-Toe-Multiplayer.git
   cd Tic-Tac-Toe-Multiplayer
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### For the Host (Server)
1. Run the server script:
   ```bash
   python server.py
   ```
2. The server will display its IP address and wait for a connection.

### For the Client
1. Run the client script with the server's IP address:
   ```bash
   python main.py <server_ip>
   ```
2. The game will connect to the server and begin when both players are ready.

## Game Controls
- Click on any empty square to place your mark (X or O)
- The game automatically detects wins and draws
- Close the window to exit the game

## Network Configuration
- Default port: 5555 (configurable in the code)
- Ensure firewalls allow traffic on the chosen port
- For local play, use 127.0.0.1 as the server IP

## Implementation Details

### Server Responsibilities:
- Maintains game state
- Validates moves
- Broadcasts game updates to clients
- Determines game outcomes

### Client Responsibilities:
- Displays the game board
- Sends player moves to the server
- Receives and renders opponent moves
- Shows game status messages

## Troubleshooting
- If connection fails, verify both machines are on the same network
- Check that firewalls aren't blocking the connection
- Ensure the server is running before clients attempt to connect
- Verify Python and all dependencies are properly installed


## License
This project is open-source and available under the MIT License.
