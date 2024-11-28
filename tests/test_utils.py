import pandas as pd
import pytest
from src.data_loader import DataLoader
from src.utils import filter_dataframebis1  # Ensure that import is correct


@pytest.fixture
def interactions_data():
    """
    Fixture that provides a DataFrame loaded with the 'RAW_recipes.csv.zip' dataset.
    
    This fixture is used across various test cases to simulate interactions data.
    
    Returns:
        pd.DataFrame: A DataFrame containing the loaded dataset.
    """
    data_loader = DataLoader()
    df = data_loader.load_data("dataset/RAW_recipes.csv.zip")
    assert not df.empty, "Loaded DataFrame should not be empty"  # Check if dataframe isn't empty
    return df


def test_filter_dataframebis1_no_matching_results(interactions_data):
    """
    Test filtering with no matching results.

    Filters the data with a tag that doesn't exist in the dataset, expecting an empty DataFrame.

    Args:
        interactions_data (pd.DataFrame): The input DataFrame to be filtered.
    """
    column_names = ["tags"]
    filter_values = ["non-existent-tag"]  
    filtered_df = filter_dataframebis1(interactions_data, column_names, filter_values)
    assert len(filtered_df) == 0  


def test_filter_dataframebis1_invalid_column(interactions_data):
    """
    Test filtering with an invalid column name.

    This test expects a KeyError to be raised when the provided column name does not exist in the DataFrame.

    Args:
        interactions_data (pd.DataFrame): The input DataFrame to be filtered.
    """
    column_names = ["invalid_column"]  
    filter_values = ["value"]
    
    with pytest.raises(KeyError):
        filter_dataframebis1(interactions_data, column_names, filter_values)


def test_filter_dataframebis1_empty_dataframe():
    """
    Test filtering on an empty DataFrame.

    This test ensures that the function handles an empty DataFrame properly and returns an empty DataFrame.
    """
    df_empty = pd.DataFrame(columns=["tags", "value"])
    column_names = ["tags"]
    filter_values = ["bio"]
    
    filtered_df = filter_dataframebis1(df_empty, column_names, filter_values)
    assert len(filtered_df) == 0  


def test_filter_dataframebis1_with_none(interactions_data):
    """
    Test filtering with None as a filter value.

    Filters the DataFrame by a None value in the 'tags' column and ensures all entries are NaN for the 'tags' column.
    
    Args:
        interactions_data (pd.DataFrame): The input DataFrame to be filtered.
    """
    column_names = ["tags"]
    filter_values = [None]  
    
    filtered_df = filter_dataframebis1(interactions_data, column_names, filter_values)
    
    
    assert all(filtered_df["tags"].isnull())  


def test_filter_dataframebis1_numeric_filter():
    """
    Test filtering on a DataFrame with numeric values.

    This test ensures that the function handles numeric filtering correctly.

    Returns:
        None
    """
    df_numeric = pd.DataFrame({
        "n_steps": [1, 2, 3, 4, 5, 6, 7],
        "categories": ["a", "b", "c", "d", "e", "f", "g"],
    })
    column_names = ["n_steps"]
    filter_values = [[1, 2, 3]]
    
    filtered_df = filter_dataframebis1(df_numeric, column_names, filter_values)
    assert len(filtered_df) == 3  


def test_filter_dataframebis1_category_filter():
    """Test filtering on a DataFrame with categorical values."""
    df_categorical = pd.DataFrame({
        "ingredients": pd.Categorical(["eggs", "sugar", "salt", "rabbit", "pepper"]),
    })
    column_names = ["ingredients"]
    filter_values = [["eggs", "pepper"]]
    
    filtered_df = filter_dataframebis1(df_categorical, column_names, filter_values)
    assert len(filtered_df) == 2  


def test_filter_dataframebis1_large_dataset():
    """
    Test filtering with a large DataFrame.

    This test ensures that the function can handle large DataFrames efficiently and filters correctly.

    Returns:
        None
    """
    large_df = pd.DataFrame({
        "tags": ["bio"] * 10000 + ["non-bio"] * 10000,
        "ingredients": ["eggs"] * 20000,
    })
    column_names = ["tags"]
    filter_values = ["bio"]
    
    filtered_df = filter_dataframebis1(large_df, column_names, filter_values)
    
    # Check that the length of filtered DataFrame matches expected size
    assert len(filtered_df) == 20000


def test_filter_dataframebis1_non_iterable_filter_values(interactions_data):
    """
    Test filtering with a non-iterable filter value.

    This test checks how the function handles a non-iterable filter value such as a string.

    Args:
        interactions_data (pd.DataFrame): The input DataFrame to be filtered.
    """
    column_names = ["tags"]
    filter_values = "bio"  # String instead of list
    filter_dataframebis1(interactions_data, column_names, filter_values)












