import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt

class TicTacToeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(100, 100, 400, 400)

        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.player1_name = ''
        self.player2_name = ''

        self.wins = {'X': 0, 'O': 0}

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.create_name_inputs()
        self.create_board()
        self.create_buttons()
        self.create_scorecard()
        self.create_turn_display()

        self.reset_button.clicked.connect(self.reset_game)
        self.reset_board_button.clicked.connect(self.reset_board)
        self.save_button.clicked.connect(self.save_names)

    def create_name_inputs(self):
        player1_layout = QHBoxLayout()
        player2_layout = QHBoxLayout()

        self.player1_label = QLabel('Player 1 Name:')
        self.player1_input = QLineEdit()
        self.player1_input.setMaximumWidth(150)  
        player1_layout.addWidget(self.player1_label)
        player1_layout.addWidget(self.player1_input)

        self.player2_label = QLabel('Player 2 Name:')
        self.player2_input = QLineEdit()
        self.player2_input.setMaximumWidth(150)  
        player2_layout.addWidget(self.player2_label)
        player2_layout.addWidget(self.player2_input)

        self.layout.addLayout(player1_layout, 0, 0, Qt.AlignLeft)
        self.layout.addLayout(player2_layout, 1, 0, Qt.AlignLeft)

    def create_board(self):
        board_container = QWidget()
        board_layout = QGridLayout(board_container)
        for i in range(3):
            for j in range(3):
                button = QPushButton('', clicked=lambda state, i=i, j=j: self.on_button_click(i, j))
                button.setStyleSheet('font-size: 30px')
                button.setFixedSize(100, 100)
                self.buttons[i][j] = button
                board_layout.addWidget(button, i, j)

        board_layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(board_container, 3, 0, 1, 2)

    def create_buttons(self):
        self.save_button = QPushButton('Save Names')
        self.reset_button = QPushButton('Reset Game')
        self.reset_board_button = QPushButton('Reset Board')

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.reset_board_button)

        self.layout.addLayout(button_layout, 2, 0, 1, 2)

    def create_scorecard(self):
        self.scorecard_label = QLabel()
        self.layout.addWidget(self.scorecard_label, 6, 0, 1, 2)

    def create_turn_display(self):
        self.turn_label = QLabel()
        self.update_turn_display()
        self.layout.addWidget(self.turn_label, 5, 0, 1, 2)

    def on_button_click(self, row, col):
        if not self.board[row][col]:
            self.board[row][col] = self.current_player
            self.buttons[row][col].setText(self.current_player)
            self.check_win()
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.update_turn_display()

    def update_scorecard(self):
        player1_wins = self.wins['X']
        player2_wins = self.wins['O']
        self.scorecard_label.setText(f'{self.player1_name}: {player1_wins} | {self.player2_name}: {player2_wins}')

    def update_turn_display(self):
        if self.player1_name and self.player2_name:
            self.turn_label.setText(f"Player's Turn: {self.player1_name if self.current_player == 'X' else self.player2_name} ({self.current_player})")
        else:
            self.turn_label.setText("")

    def check_win(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                self.show_winner(self.board[i][0])
                return
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                self.show_winner(self.board[0][i])
                return
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            self.show_winner(self.board[0][0])
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            self.show_winner(self.board[0][2])
            return
        if all(self.board[i][j] for i in range(3) for j in range(3)):
            self.show_winner('Tie')

    def show_winner(self, winner):
        winner_text = 'Tie' if winner == 'Tie' else f'{self.player1_name if winner == "X" else self.player2_name} wins!'
        message_box = QMessageBox.information(self, 'Game Over', winner_text)
        if winner != 'Tie':
            self.wins[winner] += 1
        self.update_scorecard()
        self.reset_board() 

    def reset_game(self):
        self.current_player = 'X'
        self.player1_name = self.player1_input.text()
        self.player2_name = self.player2_input.text()
        self.scorecard_label.clear()  
        self.wins = {'X': 0, 'O': 0}  
        self.reset_board()  
        self.player1_input.setReadOnly(False)  
        self.player2_input.setReadOnly(False)
        self.update_turn_display()

    def reset_board(self):
        self.current_player = 'X'
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ''
                self.buttons[i][j].setText('')
        self.update_turn_display()

    def save_names(self):
        self.player1_name = self.player1_input.text()
        self.player2_name = self.player2_input.text()
        self.update_scorecard()  
        self.player1_input.setReadOnly(True)  
        self.player2_input.setReadOnly(True)
        self.update_turn_display()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TicTacToeApp()
    window.show()
    sys.exit(app.exec_())
