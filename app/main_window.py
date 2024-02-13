import csv
import pandas as pd
from joblib import load
from PyQt5.QtGui import QFont
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QVBoxLayout, QCheckBox
from utils.DatabaseManager import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super(MainWindow, self).__init__()
        loadUi("ui/main_window.ui", self)
        self.widget = widget
        self.pushButton.clicked.connect(self.predict_disease)
        self.pushButton_2.clicked.connect(self.uncheck_all_checkboxes)
        self.model = load("ml_model/random_forest.joblib")  # Load the trained model

        # Load the symptom-severity data
        symptoms = pd.read_csv('data/Symptom-severity.csv')
        symptoms['Symptom'] = symptoms['Symptom'].str.replace('_', ' ')

        self.recommendation = pd.read_csv("data/symptom_precaution.csv")
        self.recommendation.head()

        self.description = pd.read_csv("data/symptom_Description.csv")
        self.description.head()

        # Create a dictionary mapping symptom names to their severity weights
        self.symptom_weight_map = {}
        for _, row in symptoms.iterrows():
            symptom = row['Symptom']
            weight = row['weight']
            self.symptom_weight_map[symptom] = weight

        self.load_symptoms()

    def clean_symptom_name(self, name):
        # Remove underscores and capitalize the first letter
        return name.replace("_", " ").capitalize()

    def load_symptoms(self):
        symptom_file = "data/Symptom-severity.csv"

        # Create a widget to hold checkboxes
        self.scrollAreaWidgetContents = QWidget(self.scrollArea)  # Keep a reference
        layout = QVBoxLayout(self.scrollAreaWidgetContents)

        try:
            with open(symptom_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                symptoms = [self.clean_symptom_name(row['Symptom']).capitalize() for row in
                            reader]  # Capitalize the first word

                # Sort symptoms alphabetically
                symptoms.sort()

                for symptom in symptoms:
                    checkbox = QCheckBox(symptom)

                    # Set font and remove background
                    checkbox.setStyleSheet("QCheckBox { background-color: none; }")
                    checkbox.setFont(QFont("Century Gothic", 11))

                    layout.addWidget(checkbox)

        except FileNotFoundError:
            print(f"File {symptom_file} not found.")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    def predict_disease(self):
        try:
            # Gather the checked symptoms
            checked_symptoms = []
            num_checked = 0
            for checkbox in self.scrollAreaWidgetContents.findChildren(QCheckBox):
                if checkbox.isChecked():
                    checked_symptoms.append(checkbox.text().lower())  # Make symptoms lowercase
                    num_checked += 1

            print("Checked Symptoms:", checked_symptoms)

            if num_checked < 2:
                QMessageBox.warning(self, "Not enough symptoms selected",
                                    "Please select at least two symptoms before predicting.")
                return

            elif num_checked > 17:
                QMessageBox.warning(self, "Too many symptoms selected",
                                    "Please select up to 17 symptoms before predicting.")
                return

            # Map symptoms to their weights from the symptom_index_map dictionary
            weights = [self.symptom_weight_map[symptom] if symptom in self.symptom_weight_map else 0 for symptom in
                       checked_symptoms]

            print("Symptom Weights:", weights)

            # Pad the weights list with zeros if less than 17 symptoms are selected
            padded_weights = weights + [0] * (17 - len(weights))

            print("Padded Weights:", padded_weights)

            # Make the prediction based on the padded weights
            if checked_symptoms:
                print("Model Loaded:", self.model)
                # Perform prediction using the loaded model
                predicted_disease = self.model.predict([padded_weights])[0]
                print(predicted_disease)
                disease_description = self.description[self.description['Disease'] == predicted_disease]
                disease_description = disease_description.values[0][1]

                # Display the prediction in the text browser
                self.textBrowser.setText(f"{predicted_disease}  \nDescription: {disease_description}")
            else:
                QMessageBox.warning(self, "No Symptoms Selected",
                                    "Please select at least one symptom before predicting.")

        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")
            print(f"Prediction Error: {str(e)}")

    def uncheck_all_checkboxes(self):
        # Iterate over all the checkboxes and uncheck them
        for checkbox in self.scrollAreaWidgetContents.findChildren(QCheckBox):
            checkbox.setChecked(False)
        self.textBrowser.clear()