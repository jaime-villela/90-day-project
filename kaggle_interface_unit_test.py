import unittest
from unittest.mock import patch, MagicMock
from kaggle_interface import KaggleInterface

class TestKaggleInterface(unittest.TestCase):
    @patch("kaggle_interface.os.listdir")
    @patch("kaggle_interface.zipfile.ZipFile")
    @patch("kaggle_interface.os.path.exists")
    @patch("kaggle_interface.KaggleApi")
    def test_download_dataset_file_exists(self, MockKaggleApi, mock_path_exists, MockZipFile, mock_listdir):
        # Arrange
        mock_api_instance = MockKaggleApi.return_value
        mock_api_instance.dataset_download_files = MagicMock()
        mock_path_exists.return_value = True  # Simulate that the zip file exists
        mock_zip_instance = MockZipFile.return_value
        mock_zip_instance.__enter__.return_value = mock_zip_instance
        mock_listdir.return_value = ["us-accidents.csv"]  # Simulate extracted files

        kaggle_interface = KaggleInterface()

        # Act
        result = kaggle_interface.download_dataset("sobhanmoosavi/us-accidents")

        # Assert
        mock_path_exists.assert_called_once_with("./us-accidents.zip")
        mock_api_instance.dataset_download_files.assert_not_called()  # Ensure no download happens
        MockZipFile.assert_called_once_with("./us-accidents.zip", "r")  # Verify zip file opened
        mock_zip_instance.extractall.assert_called_once_with("./")  # Verify extraction
        mock_listdir.assert_called_once_with("./")  # Verify directory listing
        self.assertEqual(result, "us-accidents.csv")  # Verify returned file path

    @patch("kaggle_interface.os.listdir")
    @patch("kaggle_interface.zipfile.ZipFile")
    @patch("kaggle_interface.os.path.exists")
    @patch("kaggle_interface.KaggleApi")
    def test_download_dataset_file_does_not_exist(self, MockKaggleApi, mock_path_exists, MockZipFile, mock_listdir):
        # Arrange
        mock_api_instance = MockKaggleApi.return_value
        mock_api_instance.dataset_download_files = MagicMock()
        mock_path_exists.return_value = False  # Simulate that the zip file does not exist
        mock_zip_instance = MockZipFile.return_value
        mock_zip_instance.__enter__.return_value = mock_zip_instance
        mock_listdir.return_value = ["us-accidents.csv"]  # Simulate extracted files

        kaggle_interface = KaggleInterface()

        # Act
        result = kaggle_interface.download_dataset("sobhanmoosavi/us-accidents")

        # Assert
        mock_path_exists.assert_called_once_with("./us-accidents.zip")
        mock_api_instance.dataset_download_files.assert_called_once_with(
            "sobhanmoosavi/us-accidents", path="./", unzip=False
        )  # Ensure download happens
        MockZipFile.assert_called_once_with("./us-accidents.zip", "r")  # Verify zip file opened
        mock_zip_instance.extractall.assert_called_once_with("./")  # Verify extraction
        self.assertEqual(result, "us-accidents.csv")  # Verify returned file path

    def test_instance_creation(self):
        # Act
        kaggle_interface = KaggleInterface()

        # Assert
        self.assertIsInstance(kaggle_interface, KaggleInterface)  # Check instance type
        self.assertTrue(hasattr(kaggle_interface, "api"))  # Check if 'api' attribute exists
        self.assertIsNotNone(kaggle_interface.api)  # Ensure 'api' is initialized

if __name__ == "__main__":
    unittest.main()