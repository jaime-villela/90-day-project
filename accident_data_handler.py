import pandas as pd
import os
import requests
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile

class AccidentDataHandler:
    """
    Base class for handling accident data downloaded from Kaggle.
    """

    def __init__(self, kaggle_url: str):
        """
        Constructor for the base class.

        :param kaggle_url: The URL of the Kaggle dataset to be downloaded.
        """
        if not kaggle_url or not isinstance(kaggle_url, str):
            raise ValueError("kaggle_url must be a non-empty string")
        self.kaggle_url = kaggle_url
        self.download_path = "./"  # Default directory for downloaded files
        self.dataframe = None
        self.api = KaggleApi()
        self.api.authenticate()

    def download_dataset(self):
        """
        Placeholder method for downloading the dataset.
        To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def load_to_dataframe(self):
        """
        Placeholder method for loading the dataset into a Pandas DataFrame.
        To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def create_accidents_per_year(self):
        """
        Placeholder method for creating a new dataset of accidents per year.
        To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")