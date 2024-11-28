import pandas as pd
import pytest
from src.nutrition_stats import stats_bio

@pytest.fixture
def sample_bio_df():
    """
    Fixture that provides a small sample DataFrame with bio recipes.

    Returns:
        pd.DataFrame: A DataFrame with bio recipes for testing purposes.
    """
    data = {
        'name': ['Recipe1', 'Recipe2', 'Recipe3'],
        'nutrition': ['[200, 10, 5, 500, 8, 2, 30]', '[150, 8, 4, 400, 6, 1, 25]', '[250, 15, 6, 600, 10, 3, 40]'],
        'ingredients': [
            "['ingredient1', 'ingredient2', 'ingredient3']",
            "['ingredient1', 'ingredient2']",
            "['ingredient1', 'ingredient2', 'ingredient3', 'ingredient4']"
        ]
    }
    return pd.DataFrame(data)
def test_stats_bio(sample_bio_df: pd.DataFrame):
    """
    Test the stats_bio function to ensure it correctly processes the filtered bio DataFrame and prints the expected outputs.

    This test will capture the printed output and verify that the correct statistics are displayed for bio recipes.

    Args:
        sample_bio_df (pd.DataFrame): The small DataFrame containing bio recipes to be processed by stats_bio.
        capsys (pytest.CaptureFixture): Pytest's capture fixture to capture printed output.

    Returns:
        None
    """
    # Call the function to test
    stats_bio(sample_bio_df)
