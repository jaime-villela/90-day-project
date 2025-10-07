# test_accident_data_handler.py
import unittest
from unittest.mock import patch, MagicMock
from accident_data_handler import AccidentDataHandler

class TestAccidentDataHandler(unittest.TestCase):
    def setUp(self):
        # Create a subclass for testing purposes
        class TestHandler(AccidentDataHandler):
            def download_dataset(self):
                return "Dataset downloaded"

            def load_to_dataframe(self):
                return "Data loaded into DataFrame"

        self.handler = TestHandler(kaggle_url="https://example.com/dataset")

    def test_initialization(self):
        # Test that attributes are set correctly
        self.assertEqual(self.handler.kaggle_url, "https://example.com/dataset")
        self.assertEqual(self.handler.download_path, "./")
        self.assertIsNone(self.handler.dataframe)

    def test_invalid_initialization(self):
        # Test that initializing with an invalid URL raises an error
        with self.assertRaises(ValueError):
            AccidentDataHandler(kaggle_url="")

    def test_abstract_methods(self):
        # Test that abstract methods raise NotImplementedError in the base class
        with self.assertRaises(NotImplementedError):
            AccidentDataHandler("https://example.com").download_dataset()
        with self.assertRaises(NotImplementedError):
            AccidentDataHandler("https://example.com").load_to_dataframe()

    def test_subclass_methods(self):
        # Test that subclass methods work as expected
        self.assertEqual(self.handler.download_dataset(), "Dataset downloaded")
        self.assertEqual(self.handler.load_to_dataframe(), "Data loaded into DataFrame")

    def test_download_path_modification(self):
        # Test that the download_path attribute can be modified
        self.handler.download_path = "new_data_path"
        self.assertEqual(self.handler.download_path, "new_data_path")

    @patch("accident_data_handler.KaggleApi")
    def test_constructor_with_valid_kaggle_url(self, mock_api):
        # Arrange
        mock_api_instance = MagicMock()
        mock_api.return_value = mock_api_instance
        valid_url = "https://www.kaggle.com/datasets/some-dataset"

        # Act
        handler = AccidentDataHandler(valid_url)

        # Assert
        self.assertEqual(handler.kaggle_url, valid_url)
        self.assertEqual(handler.download_path, "./")
        self.assertIsNone(handler.dataframe)
        mock_api.assert_called_once()  # Ensure KaggleApi is instantiated
        mock_api_instance.authenticate.assert_called_once()  # Ensure authenticate is called

    def test_constructor_with_invalid_kaggle_url(self):
        # Arrange
        invalid_url = ""

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            AccidentDataHandler(invalid_url)
        self.assertEqual(str(context.exception), "kaggle_url must be a non-empty string")

if __name__ == "__main__":
    unittest.main()