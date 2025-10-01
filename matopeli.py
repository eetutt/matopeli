# 'pip install PySide6' tarvitaan 
import sys
import random

from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMenu
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor
from PySide6.QtCore import Qt, QTimer
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl

# vakiot
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)

        self.crash_sound = QSoundEffect()
        self.crash_sound.setSource(QUrl.fromLocalFile("crash.wav"))
        self.food_sound = QSoundEffect()
        self.food_sound.setSource(QUrl.fromLocalFile("apple_crunch.wav"))

        self.game_started = False
        self.init_screen()
    def init_screen(self):
        self.scene().clear()
        font = QFont("Arial", 18)
        start_text = self.scene().addText("Press any key to start", font)
        text_rect = start_text.boundingRect()
        view_width = self.viewport().width()
        view_height = self.viewport().height()
        text_x = (view_width - text_rect.width()) / 2
        text_y = (view_height - text_rect.height()) / 2
        start_text.setPos(text_x, text_y)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.game_started:
            self.init_screen()
        elif self.game_started and not self.timer.isActive():
            self.show_game_over()

    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return x, y

    def keyPressEvent(self, event):
        key = event.key()
        if not self.game_started:
            self.game_started = True
            self.scene().clear()
            self.start_game()
            return
        if hasattr(self, 'waiting_new_game') and self.waiting_new_game:
            self.waiting_new_game = False
            self.game_started = True
            self.scene().clear()
            self.start_game()
            return
        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            if key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = key
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = key
            elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = key
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = key

    def update_game(self):
        head_x, head_y = self.snake[0]

        if self.direction == Qt.Key_Left:
            new_head = (head_x - 1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x + 1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y - 1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y + 1)

        # board limits
        if new_head in self.snake or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
            self.timer.stop()
            self.crash_sound.play()
            self.show_game_over()
            self.game_started = False
            return

        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 1
            self.food_sound.play()
            self.food = self.spawn_food()
            if self.score == self.level_limit:
                self.level_limit += 5
                self.timer_delay *= 0.9
                self.timer.setInterval(self.timer_delay)

        else:
            self.snake.pop()

        self.print_game()

    def print_game(self):
        self.scene().clear()
        view_width = self.viewport().width()
        view_height = self.viewport().height()
        for i in range(int(view_width/CELL_SIZE)):
            for j in range(int(view_height/CELL_SIZE)):
                self.scene().addRect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(QColor(220,220,220))), QBrush(QColor(200, 200, 200))

        #self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT)
        for segment in self.snake:
            x, y = segment
            self.scene().addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(QColor(0,80,0)), QBrush(QColor(40, 160, 0)))
            fx, fy = self.food
            self.scene().addRect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(QColor(80,0,0)), QBrush(Qt.red))
            self.scene().addText(f"Score: {self.score}", QFont("Arial", 12)) 
        
    def start_game(self):
        #pisteen laskentaa varten
        self.score = 0
        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.timer.start(300)
        self.food = self.spawn_food()
        self.game_started = True
        if hasattr(self, 'waiting_new_game'):
            self.waiting_new_game = False
            # for levels
        self.level_limit = 5
        self.timer_delay = 300

        self.timer.start(self.timer_delay)

    def show_game_over(self):
        self.scene().clear()
        font = QFont("Arial", 18)
        over_text = self.scene().addText("Game Over, start new game?", font)
        text_rect = over_text.boundingRect()
        view_width = self.viewport().width()
        view_height = self.viewport().height()
        text_x = (view_width - text_rect.width()) / 2
        text_y = (view_height - text_rect.height()) / 2
        over_text.setPos(text_x, text_y)
        self.waiting_new_game = True

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()