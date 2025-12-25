# Standard Imports
import logging

# Third-party Imports
import numpy as np
import pandas as pd

# Configure logger
logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.INFO)

# Create handler
if not logger.handlers:

    handler = logging.StreamHandler()

    # Configure formatter and add to handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_logger() -> logging.Logger:
    """
    Function to get initialised logger object.
    """
    return logger


def simulate_large_dataset() -> pd.DataFrame:
    """
    Generates a large numerical dataset and returns it as a dataframe.

    Parameters:
    - None

    Returns:
    - pd.DataFrame: Pandas dataframe containing generated data.
    """
    df = pd.DataFrame(
        {
            "col1": np.random.randn(20_000),
            "col2": np.random.randn(20_000),
            "col3": np.random.randint(0, 100, 20_000),
        }
    )

    return df
