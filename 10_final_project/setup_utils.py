import os
import json
from pathlib import Path
import zipfile

"""Helper utility functions for w Jupyter notebooks in Local and Remote environment.

This module contains various utility functions to ease the work in Jupyter notebooks.
It contains functions for environment checks, installing libraries, setting up Kaggle credentials, 
and downloading datasets from Kaggle.

Author:
    Jesper Alkestrup <jalkestrup At gmail DOT com>
"""


def check_environment() -> bool:
    """Check if the notebook is running in Google Colab or not.

    Returns:
        bool: True if running in Colab, False otherwise.
    """
    return bool(os.getenv("COLAB_RELEASE_TAG"))


def install_libraries(colab_flag: bool):
    """Install required libraries based on the environment.

    Args:
        colab_flag (bool): Indicates if the notebook is running in Google Colab.

    Returns:
        None
    """
    if colab_flag:
        print("Running in Colab...")
        os.system("pip install -q kaggle")
        os.system("pip install -q datasets")
        os.system("pip install -q transformers[torch]")
        os.system("pip install -q timm")
        print("...Installed required dependencies")
    else:
        print("Running in local environment...")


def set_kaggle_credentials(colab_flag: bool):
    """Set Kaggle API credentials.

    Args:
        colab_flag (bool): Indicates if the notebook is running in Google Colab.

    Returns:
        None
    """

    if colab_flag:
        from google.colab import drive

        drive.mount("/content/drive/")
        file_path = "/content/drive/MyDrive/dtu/fastAI/kaggle_api.json"
    else:
        file_path = "../secrets/kaggle_api.json"

    if os.path.exists(file_path):
        with open(file_path) as f:
            creds = json.load(f)
        print("Sucesfully set kaggle credentials")
    else:
        print("Error: File not found, Credentials NOT set")


def download_kaggle_data(dataset_name: str):
    """Download dataset from Kaggle.

    Args:
        dataset_name (str): The Kaggle dataset name (usually a path-like string).

    Returns:
        None
    """
    path = Path(dataset_name)
    if path.exists():
        print("Data folder already exists")
    else:
        print("Data not detected, starting download")
        cred_path = Path("~/.kaggle/kaggle.json").expanduser()
        if not cred_path.exists():
            print(
                "Error: Kaggle credentials not set. Please set them before downloading data."
            )
            return
        cred_path.chmod(0o600)
        import kaggle

        kaggle.api.competition_download_cli(dataset_name)
        zipfile.ZipFile(f"{dataset_name}.zip").extractall(path)
