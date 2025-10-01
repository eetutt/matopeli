
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt
import sys

class TestView(QGraphicsView):
    def __init__(self):
        super().__init__()

        scene = QGraphicsScene(self)
        scene.setSceneRect(0, 0, 400, 300)
        scene.setBackgroundBrush(QBrush(Qt.white))

        self.setScene(scene)
        self.setBackgroundBrush(Qt.NoBrush)
        self.setAutoFillBackground(False)
        self.setFixedSize(402, 302)

        # Add a colored rectangle to test
        scene.addRect(50, 50, 100, 100, QPen(Qt.black), QBrush(Qt.red))

app = QApplication(sys.argv)
view = TestView()
view.show()
sys.exit(app.exec())