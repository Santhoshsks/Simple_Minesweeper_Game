import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import sys

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minesweeper By Santhosh SSK")
        self.setGeometry(100, 100, 730, 820)
        self.UiComponents()
        self.show()
        self.grid_size = (8, 8)
        self.num_bombs = 10
        self.game_grid = None
        self.revealed_cells = None
        self.flagged_cells = None
        self.initialize_game()

    def initialize_game(self):
        self.game_grid = np.zeros(self.grid_size, dtype=int)
        self.revealed_cells = np.zeros(self.grid_size, dtype=bool)
        self.flagged_cells = np.zeros(self.grid_size, dtype=bool)
        bombs = np.random.choice(self.grid_size[0] * self.grid_size[1], self.num_bombs, replace=False)
        for bomb in bombs:
            row = bomb // self.grid_size[1]
            col = bomb % self.grid_size[1]
            self.game_grid[row, col] = -1
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.grid_size[0] and 0 <= c < self.grid_size[1] and self.game_grid[r, c] != -1:
                        self.game_grid[r, c] += 1

    def reveal_cell(self, row, col):
        if self.revealed_cells[row, col] or self.flagged_cells[row, col]:
            return
        self.revealed_cells[row, col] = True
        if self.game_grid[row, col] == -1:
            self.show_lost_message()
            self.enable_buttons()
        elif self.game_grid[row, col] == 0:
            self.reveal_empty_cells(row, col)
        self.update_ui()

    def reveal_empty_cells(self, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.grid_size[0] and 0 <= c < self.grid_size[1] and not self.revealed_cells[r, c]:
                    self.reveal_cell(r, c)

    def flag_cell(self, row, col):
        if not self.revealed_cells[row, col]:
            self.flagged_cells[row, col] = not self.flagged_cells[row, col]
            self.update_ui()

    def show_lost_message(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Game Over")
        message_box.setText("You lost! Click Reset to play again")
        message_box.exec_()

    def action_called(self):
        button = self.sender()
        row, col = self.get_button_position(button)
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.flag_cell(row, col)
        else:
            self.reveal_cell(row, col)
        self.update_ui()
        self.check_game_state()

    def get_button_position(self, button):
        for i, row_buttons in enumerate(self.push_list):
            for j, btn in enumerate(row_buttons):
                if btn == button:
                    return i, j
        return None, None

    def update_ui(self):
        for i in range(8):
            for j in range(8):
                if self.revealed_cells[i, j]:
                    if self.game_grid[i, j] == -1:
                        self.push_list[i][j].setText("B")
                    elif self.game_grid[i, j] == 0:
                        self.push_list[i][j].setText("")
                    else:
                        self.push_list[i][j].setText(str(self.game_grid[i, j]))
                    self.push_list[i][j].setEnabled(False)
                elif self.flagged_cells[i, j]:
                    self.push_list[i][j].setText("F")
                else:
                    self.push_list[i][j].setText("")
                    self.push_list[i][j].setEnabled(True)

    def reset_game_action(self):
        self.initialize_game()
        self.update_ui()
        self.label.setText("")
        self.enable_buttons()

    def enable_buttons(self):
        for buttons in self.push_list:
            for button in buttons:
                button.setEnabled(True)

    def check_game_state(self):
        if np.all(self.revealed_cells) or np.all(self.flagged_cells):
            self.enable_buttons()
            self.show_win_message()

    def show_win_message(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Congratulations")
        message_box.setText("You won! Click Reset to play again")
        message_box.exec_()

    def UiComponents(self):
        self.push_list = []

        for _ in range(8):
            temp = []
            for _ in range(8):
                temp.append(QPushButton(self))
            self.push_list.append(temp)

        x = 90
        y = 90

        for i in range(8):
            for j in range(8):
                self.push_list[i][j].setGeometry(x * j + 5, y * i + 5, 90, 90)
                self.push_list[i][j].setFont(QFont(QFont('Times', 17)))
                self.push_list[i][j].clicked.connect(self.action_called) 

        self.label = QLabel(self)
        self.label.setGeometry(80, y * 8 + 20, 300, 70) 

        reset_game = QPushButton("Reset", self)
        reset_game.setGeometry(190, y * 8 + 20, 300, 70)
        reset_game.clicked.connect(self.reset_game_action)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())
