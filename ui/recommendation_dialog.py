from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout


class RecommendationDialog(QDialog):
    def __init__(self, recommendation_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recommendation")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # Remove the question mark button

        layout = QVBoxLayout()

        recommendation_label = QLabel(recommendation_text)
        layout.addWidget(recommendation_label)

        self.setLayout(layout)

        # Apply background color
        self.setStyleSheet("background-color: #a5d9c7;")