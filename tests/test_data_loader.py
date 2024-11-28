import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
from src.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.data_loader = DataLoader()

    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("os.listdir")
    @patch("src.data_loader.zipfile.ZipFile")
    def test_unzip_data_zipfile(self, mock_zipfile, mock_listdir, mock_makedirs, mock_exists):
        """
            Test the extraction of ZIP files.

            This test checks that ZIP files are extracted correctly using the zipfile module
            and verifies the creation of the appropriate directory and extracted file paths.
        """
        mock_exists.return_value = False
        mock_listdir.return_value = ["file1.csv", "file2.csv"]

        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        file_name = "test.zip"
        result = self.data_loader.unzip_data(file_name)

        mock_zip.extractall.assert_called_once()
        mock_makedirs.assert_called_once_with("test_extracted")
        self.assertEqual(result, ["test_extracted/file1.csv", "test_extracted/file2.csv"])

    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("os.listdir")
    @patch("src.data_loader.DataLoader.decompress_xz")
    def test_unzip_data_xzfile(self, mock_decompress_xz, mock_listdir, mock_makedirs, mock_exists):
        """
            Test the decompression of XZ files.

            Ensures that the decompress_xz method is called correctly and that the output file
            paths match the expected results.
        """
        mock_exists.return_value = False
        mock_listdir.return_value = ["file1.csv"]
        mock_decompress_xz.return_value = "test_extracted/file1.csv"

        file_name = "test.xz"
        result = self.data_loader.unzip_data(file_name)

        mock_decompress_xz.assert_called_once_with(file_name, "test_extracted")
        mock_makedirs.assert_called_once_with("test_extracted")
        self.assertEqual(result, ["test_extracted/file1.csv"])

    @patch("pandas.read_csv")
    @patch("src.data_loader.DataLoader.unzip_data")
    def test_load_data_from_zip(self, mock_unzip_data, mock_read_csv):
        """
            Test loading data from a ZIP archive containing CSV files.

            Verifies that the data is correctly unzipped and loaded into a pandas DataFrame.
        """
        mock_unzip_data.return_value = ["file1.csv"]
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_csv.return_value = mock_df

        file_name = "test.zip"
        result = self.data_loader.load_data(file_name)

        mock_unzip_data.assert_called_once_with(file_name)
        mock_read_csv.assert_called_once_with("file1.csv")
        pd.testing.assert_frame_equal(result, mock_df)

    @patch("pandas.read_csv")
    def test_load_data_from_csv(self, mock_read_csv):
        """
            Test loading data directly from a CSV file.

            Ensures that pandas' read_csv function is called and that the DataFrame
            matches the expected structure and content.
        """
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_csv.return_value = mock_df

        file_name = "test.csv"
        result = self.data_loader.load_data(file_name)

        mock_read_csv.assert_called_once_with(file_name)
        pd.testing.assert_frame_equal(result, mock_df)

    @patch("pandas.read_pickle")
    def test_load_data_from_pickle(self, mock_read_pickle):
        """
            Test loading data from a Pickle file.

            Ensures that pandas' read_pickle function correctly loads the data into
            a DataFrame with the expected content.
        """
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_pickle.return_value = mock_df

        file_name = "test.pkl"
        result = self.data_loader.load_data(file_name)

        mock_read_pickle.assert_called_once_with(file_name)
        pd.testing.assert_frame_equal(result, mock_df)

    @patch("pandas.read_csv")
    @patch("src.data_loader.DataLoader.unzip_data")
    def test_load_data_from_xz(self, mock_unzip_data, mock_read_csv):
        """
         Test loading data from an XZ archive containing CSV files.

          Verifies that the data is unzipped and loaded into a pandas DataFrame as expected.
        """
        mock_unzip_data.return_value = ["test_extracted/file1.csv"]
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_csv.return_value = mock_df

        file_name = "test.xz"
        result = self.data_loader.load_data(file_name)

        mock_unzip_data.assert_called_once_with(file_name)
        mock_read_csv.assert_called_once_with("test_extracted/file1.csv")
        pd.testing.assert_frame_equal(result, mock_df)

    def test_load_data_unsupported_file_type(self):
        """
            Test handling of unsupported file types in load_data.

            Ensures that a ValueError is raised when attempting to load an unsupported file type.
        """
        file_name = "test.txt"
        with self.assertRaises(ValueError) as context:
            self.data_loader.load_data(file_name)
        self.assertEqual(str(context.exception), f"Unsupported file type: {file_name}")
    
    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_unzip_data_unsupported_file_type(self, mock_makedirs, mock_exists):
        """
        Test handling of unsupported file types in unzip_data.

        Ensures that a ValueError is raised when attempting to unzip an unsupported file type.
        """
        mock_exists.return_value = False
        file_name = "test.unsupported"

        with self.assertRaises(ValueError) as context:
            self.data_loader.unzip_data(file_name)

        self.assertEqual(str(context.exception), f"Unsupported file type for {file_name}")

