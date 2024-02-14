from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QPushButton, QMenu, QAction, QMessageBox


class PredictionWidgetItem(QWidget):
    def __init__(self, prediction_id, prediction_text, prediction_symptoms, prediction_time, delete_callback, parent=None):
        super().__init__(parent)
        try:
            self.prediction_id = prediction_id  # Store the prediction ID
            layout = QHBoxLayout()
            self.setLayout(layout)

            # Create a vertical layout for prediction information
            prediction_layout = QVBoxLayout()

            # Prediction text label
            self.prediction_text_label = QLabel(prediction_text)
            self.prediction_text_label.setContentsMargins(0, 0, 0, 10)  # No bottom margin
            prediction_layout.addWidget(self.prediction_text_label)

            # Prediction symptoms label
            self.prediction_symptoms_label = QLabel(f"Symptoms: {prediction_symptoms}")
            self.prediction_symptoms_label.setContentsMargins(0, 0, 0, 10)  # No bottom margin
            prediction_layout.addWidget(self.prediction_symptoms_label)

            # Prediction time label
            formatted_time = prediction_time.strftime("%d.%m.%Y %H:%M")
            self.prediction_time_label = QLabel(f"Time: {formatted_time}")
            self.prediction_time_label.setContentsMargins(0, 0, 0, 10)  # Add bottom margin
            prediction_layout.addWidget(self.prediction_time_label)

            layout.addLayout(prediction_layout)

            # Delete button
            self.delete_button = QPushButton("Delete")
            self.delete_button.setFixedSize(100, 30)  # Set a fixed size for the delete button
            self.delete_button.setStyleSheet('''
                QPushButton {
                    background-color: #d24d57; /* Green background color */
                    border: 2px solid #af4154; /* Border color */
                    color: #ffffff; /* Text color */
                    padding: 8px 16px; /* Padding */
                    border-radius: 4px; /* Border radius */
                    font-family: "Century Gothic";
                    font-size: 10pt; /* Font size */
                }

                QPushButton:hover {
                    background-color: #f1828d; 
                }

                QPushButton:pressed {
                    background-color: #96281b; /* Clicked background color */
                }
            ''')
            layout.addWidget(self.delete_button, alignment=Qt.AlignRight)

            # Set widget properties
            self.setMouseTracking(True)  # Enable mouse tracking to capture mouse events
            self.setStyleSheet("QWidget:hover { background-color: none; }")  # Remove hover effect

            # Connect delete button clicked signal to delete_callback slot
            self.delete_button.clicked.connect(lambda: delete_callback(prediction_id))

            # Context menu
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.show_context_menu)

        except Exception as e:
            print(f"Error: {str(e)}")

    def get_prediction_id(self):
        return self.prediction_id

    def show_context_menu(self, pos):
        menu = QMenu(self)
        display_recommendation_action = QAction("Display Recommendation", self)
        display_recommendation_action.triggered.connect(self.display_recommendation)
        menu.addAction(display_recommendation_action)

        # Set background color of context menu
        menu.setStyleSheet("background-color: #81cfe0;")

        menu.exec_(self.mapToGlobal(pos))

    def display_recommendation(self):
        # Show recommendation dialog
        recommendation_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        QMessageBox.information(self, "Recommendation", recommendation_text)