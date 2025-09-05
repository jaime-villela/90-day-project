import unittest
from unittest.mock import patch, MagicMock
from kaggle_interface import KaggleInterface
import pandas as pd

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

    @patch("kaggle_interface.zipfile.ZipFile")
    @patch("kaggle_interface.KaggleApi")
    def test_download_single_file_from_dataset_zip_file(self, MockKaggleApi, MockZipFile):
        # Arrange
        mock_api_instance = MockKaggleApi.return_value
        mock_api_instance.dataset_download_file = MagicMock()
        mock_zip_instance = MockZipFile.return_value
        mock_zip_instance.__enter__.return_value = mock_zip_instance
        mock_zip_instance.namelist.return_value = ["extracted_file.xlsx"]  # Simulate extracted file

        kaggle_interface = KaggleInterface()

        # Act
        result = kaggle_interface.download_single_file_from_dataset("dataset-name", "file.zip")

        # Assert
        mock_api_instance.dataset_download_file.assert_called_once_with(
            "dataset-name", "file.zip", path=kaggle_interface.download_path, unzip=False
        )
        MockZipFile.assert_called_once_with("./file.zip", "r")  # Verify zip file opened
        mock_zip_instance.extractall.assert_called_once_with("./")  # Verify extraction
        self.assertEqual(result, "extracted_file.xlsx")  # Verify returned file name

    @patch("kaggle_interface.KaggleApi")
    def test_download_single_file_from_dataset_non_zip_file(self, MockKaggleApi):
        # Arrange
        mock_api_instance = MockKaggleApi.return_value
        mock_api_instance.dataset_download_file = MagicMock()

        kaggle_interface = KaggleInterface()

        # Act
        result = kaggle_interface.download_single_file_from_dataset("dataset-name", "file.xlsx")

        # Assert
        mock_api_instance.dataset_download_file.assert_called_once_with(
            "dataset-name", "file.xlsx", path=kaggle_interface.download_path, unzip=False
        )
        self.assertEqual(result, "file.xlsx")  # Verify returned file name

    def test_instance_creation(self):
        # Act
        kaggle_interface = KaggleInterface()

        # Assert
        self.assertIsInstance(kaggle_interface, KaggleInterface)  # Check instance type
        self.assertTrue(hasattr(kaggle_interface, "api"))  # Check if 'api' attribute exists
        self.assertIsNotNone(kaggle_interface.api)  # Ensure 'api' is initialized

    @patch("kaggle_interface.pd.read_csv")
    def test_load_csv_to_dataframe(self, mock_read_csv):
        # Arrange
        mock_dataframe = MagicMock(spec=pd.DataFrame)
        mock_read_csv.return_value = mock_dataframe
        kaggle_interface = KaggleInterface()
        csv_file = "test.csv"

        # Act
        result = kaggle_interface.load_csv_to_dataframe(csv_file)

        # Assert
        mock_read_csv.assert_called_once_with(csv_file)  # Verify read_csv is called with the correct file
        self.assertEqual(result, mock_dataframe)  # Verify the returned DataFrame is as expected

    @patch("kaggle_interface.pd.read_excel")
    def test_load_excel_to_dataframe(self, mock_read_excel):
        # Arrange
        mock_dataframe = MagicMock(spec=pd.DataFrame)
        mock_read_excel.return_value = mock_dataframe
        kaggle_interface = KaggleInterface()
        excel_file = "test.xlsx"

        # Act
        result = kaggle_interface.load_excel_to_dataframe(excel_file)

        # Assert
        mock_read_excel.assert_called_once_with(excel_file)  # Verify read_excel is called with the correct file
        self.assertEqual(result, mock_dataframe)  # Verify the returned DataFrame is as expected

if __name__ == "__main__":
    unittest.main()