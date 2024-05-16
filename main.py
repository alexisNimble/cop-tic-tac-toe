from flask import Flask, render_template, request, redirect, url_for
from typing import List, Optional

app = Flask(__name__)

class Player:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol

class TicTacToe:
    """
    Represents a Tic-Tac-Toe game.

    Attributes:
        board (List[List[str]]): The game board represented as a 3x3 grid.
        players (List[Player]): The list of players participating in the game.
        current_player (Optional[Player]): The player who is currently making a move.
    """

    def __init__(self):
        self.board: List[List[str]] = [['', '', ''], ['', '', ''], ['', '', '']]
        self.players: List[Player] = []
        self.current_player: Optional[Player] = None

    def add_player(self, name: str, symbol: str) -> None:
        """
        Adds a player to the game.

        Args:
            name (str): The name of the player.
            symbol (str): The symbol representing the player's moves on the board.

        Returns:
            None
        """
        player = Player(name, symbol)
        self.players.append(player)
        if self.current_player is None:
            self.current_player = player

    def switch_player(self) -> None:
        """
        Switches the current player to the next player in the list.

        Returns:
            None
        """
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def check_winner(self) -> Optional[str]:
        """
        Checks if there is a winner in the current state of the game.

        Returns:
            Optional[str]: The symbol of the winning player, 'Tie' if it's a tie, or None if there is no winner yet.
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return row[0]
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        # Check for tie
        if all(cell != '' for row in self.board for cell in row):
            return 'Tie'
        return None

    def move(self, row: int, col: int) -> None:
        """
        Makes a move on the game board.

        Args:
            row (int): The row index of the cell to make the move.
            col (int): The column index of the cell to make the move.

        Raises:
            Exception: If there is no current player set.

        Returns:
            None
        """
        if self.current_player is None:
            raise Exception("No current player set")
        # Make the move if the cell is empty
        if self.board[row][col] == '':
            self.board[row][col] = self.current_player.symbol
            self.switch_player()

game = TicTacToe()
game.add_player('Player 1', 'X')
game.add_player('Player 2', 'O')

@app.route('/')
def index() -> str:
    winner = game.check_winner()
    game_status = 'Game Over. Winner: ' + winner if winner else 'Game On'
    return render_template('index.html', board=game.board, winner=winner, game_status=game_status)

@app.route('/move', methods=['POST'])
def move() -> str:
    row = request.form.get('row')
    col = request.form.get('col')
    if row is not None and col is not None:
        game.move(int(row), int(col))
        return redirect(url_for('index'))
    else:
        return "Invalid move", 400

@app.route('/reset', methods=['POST'])
def reset() -> str:
    game.board = [['', '', ''], ['', '', ''], ['', '', '']]
    game.current_player = game.players[0]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()