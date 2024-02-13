import unittest
from joblib import load
import numpy as np

class TestMLModel(unittest.TestCase):
    def setUp(self):
        self.model = load("../ml_model/random_forest.joblib")  # Load the trained model

    def test_prediction_less_than_one_feature(self):
        # Test case: Input data with only 1 feature (less than 2 features)
        input_data_less_than_two_features = np.array([[]])  # Convert to 2D array
        with self.assertRaises(ValueError):
            self.model.predict(input_data_less_than_two_features)

    def test_prediction_more_than_seventeen_features(self):
        # Test case: Input data with 18 features (more than 17 features)
        input_data_more_than_seventeen_features = np.array([[4, 6, 3, 6, 2, 4, 3, 4, 2, 4, 4, 5, 5, 5, 4, 5, 4, 2]])  # Convert to 2D array
        with self.assertRaises(ValueError):
            self.model.predict(input_data_more_than_seventeen_features)

    def test_model_prediction(self):
        # Test case: Input data with 5 features
        input_data_5_features = np.array([[4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        expected_output_5_features = "Bronchial Asthma"
        predictions_5_features = self.model.predict(input_data_5_features)[0]
        self.assertEqual(predictions_5_features, expected_output_5_features)


if __name__ == '__main__':
    unittest.main()
