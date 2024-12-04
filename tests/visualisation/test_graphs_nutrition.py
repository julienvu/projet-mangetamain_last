import pytest
import pandas as pd
import plotly.graph_objects as go
from src.visualisation.graphs_nutrition import plot_top_4_recipes_by_nutrition, nutrition_bar_ratio_sodium_proteins  


@pytest.fixture
def sample_combined_df():
    """
    Fixture to create a sample DataFrame for testing nutritional data analysis.

    This function generates a mock dataset designed for testing purposes. It simulates
    a collection of recipes, each with various nutritional components such as calories,
    fats, sugars, sodium, proteins, and carbohydrates. The dataset structure resembles 
    what one might expect in real-world recipe data, making it useful for testing 
    data transformations, feature engineering, and analytics workflows.

    Returns:
        pandas.DataFrame: A DataFrame containing the following columns:
        
        - 'name': Names of the recipes (string).
        - 'Calories': Caloric content of each recipe (integer, in kcal).
        - 'Total Fat (g)': Total fat content (integer, in grams).
        - 'Sugar (g)': Sugar content (integer, in grams).
        - 'Sodium (mg)': Sodium content (integer, in milligrams).
        - 'Protein (g)': Protein content (integer, in grams).
        - 'Saturated Fat (g)': Saturated fat content (integer, in grams).
        - 'Carbohydrates (g)': Total carbohydrate content (integer, in grams).

    Example:
        >>> df = sample_combined_df()
        >>> print(df.head())
            name  Calories  Total Fat (g)  Sugar (g)  Sodium (mg)  Protein (g)  Saturated Fat (g)  Carbohydrates (g)
        0  Recipe A       500             20           5           300            10                  5                 60
        1  Recipe B       450             25          10           400            20                  7                 50
        2  Recipe C       600             30          15           500            30                  9                 70

    Note:
        This fixture is useful for unit tests involving data manipulation or 
        statistical analysis where real-world datasets are too large or complex to handle.
    """
    data = {
        'name': ['Recipe A', 'Recipe B', 'Recipe C', 'Recipe D', 'Recipe E', 'Recipe F'],
        'Calories': [500, 450, 600, 300, 200, 700],
        'Total Fat (g)': [20, 25, 30, 15, 10, 35],
        'Sugar (g)': [5, 10, 15, 5, 1, 25],
        'Sodium (mg)': [300, 400, 500, 200, 100, 600],
        'Protein (g)': [10, 20, 30, 15, 5, 25],
        'Saturated Fat (g)': [5, 7, 9, 2, 1, 10],
        'Carbohydrates (g)': [60, 50, 70, 40, 30, 80]
    }
    return pd.DataFrame(data)


def test_plot_top_4_recipes_by_nutrition(sample_combined_df: pd.DataFrame):
    """
    Test the `plot_top_4_recipes_by_nutrition` function from the `graphs_nutrition` module.
    
    Purpose:
    This function verifies that the `plot_top_4_recipes_by_nutrition` correctly generates
    individual `plotly.graph_objects.Figure` objects for each nutritional category.

    Parameters:
    - sample_combined_df (pd.DataFrame): A fixture that provides a sample DataFrame containing
      recipe nutritional data (e.g., Calories, Fat, Sugar).

    Steps:
    1. Calls the `plot_top_4_recipes_by_nutrition` function with the test DataFrame.
    2. Checks if the returned value is a dictionary where the keys are nutritional categories.
    3. Asserts that the dictionary contains exactly 7 figures, corresponding to the 7 nutrition categories.
    4. Ensures each figure is a valid `go.Figure` instance from the Plotly library.
    5. Verifies that the title of the figure for the "Calories" category is set correctly.

    Expected Results:
    - The function should return a dictionary with 7 keys, one for each nutritional category.
    - Each value in the dictionary should be a valid `go.Figure` object.
    - The title for the "Calories" figure should be "Top 4 Recipes by Calories".

    Assertions:
    - `isinstance(fig, dict)` ensures the output is a dictionary.
    - `len(fig) == expected_traces` checks that 7 figures are present.
    - `isinstance(fig[category], go.Figure)` verifies each category is a valid Plotly figure.
    - `fig["Calories"].layout.title.text` ensures the title is correct for one sample figure.
    """
    categories = [
    "Calories",
    "Total Fat (g)",
    "Sugar (g)",
    "Sodium (mg)",
    "Protein (g)",
    "Saturated Fat (g)",
    "Carbohydrates (g)",
    ]
    fig = plot_top_4_recipes_by_nutrition(sample_combined_df, categories)

    # Check if the figure is an instance of list
    assert isinstance(fig, dict) 

    # Check if the figure contains the expected number of traces (7 for each category)
    expected_traces = 7  # One trace per nutritional component
    assert len(fig) == expected_traces

    # Check if a figure is generated for each category
    assert len(fig) == len(categories)

    # Check if the figure for each category is an instance of go.Figure
    for category in categories:
        assert isinstance(fig[category], go.Figure)

    # Optionally, check if the layout title for one of the figures is correct
    assert fig["Calories"].layout.title.text == "Top 4 Recipes by Calories"


def test_nutrition_bar_ratio_sodium_proteins(sample_combined_df: pd.DataFrame):
    """
    Test the `nutrition_bar_ratio_sodium_proteins` function from the `graphs_nutrition` module.

    Purpose:
    This function verifies that `nutrition_bar_ratio_sodium_proteins` generates bar chart figures
    comparing ratios of nutritional components (Protein, Sodium, and Carbohydrates) for the top 4 recipes.

    Parameters:
    - sample_combined_df (pd.DataFrame): A sample DataFrame containing recipe nutritional data.

    Steps:
    1. Calls the `nutrition_bar_ratio_sodium_proteins` function with the test DataFrame and nutrition categories.
    2. Ensures the function returns a dictionary where keys are nutritional categories.
    3. Checks that the length of the dictionary matches the number of specified categories (3 in this case).
    4. Confirms that each value in the dictionary is a `plotly.graph_objects.Figure`.
    5. Verifies that the title of the "Protein (g)" figure is correct.

    Expected Results:
    - The function should return a dictionary with 4 keys: "Protein (g)", "Sodium (mg)", "Carbohydrates (g)" and "Saturated fat (g)".
    - Each figure should be a valid `go.Figure` instance.
    - The title for the "Protein (g)" figure should be "Ratios for Top 4 Recipes by Protein (g)".

    Assertions:
    - `isinstance(fig, dict)` checks that the output is a dictionary.
    - `len(fig) == len(categories)` ensures the dictionary has entries for all provided categories.
    - `isinstance(fig[category], go.Figure)` confirms each category maps to a valid Plotly figure.
    - `fig["Protein (g)"].layout.title.text` validates the title for the "Protein (g)" figure.
    """
    categories = ["Protein (g)", "Sodium (mg)", "Saturated Fat (g)", "Carbohydrates (g)"]

    # Call the function
    fig = nutrition_bar_ratio_sodium_proteins(sample_combined_df, categories)

    # Check if the figure is an instance of dict
    assert isinstance(fig, dict)

    # Check if the figure contains the expected number of categories
    assert len(fig) == len(categories)

    # Check if the figure for each category is an instance of go.Figure
    for category in categories:
        assert category in fig  # Ensure category exists in the output
        assert isinstance(fig[category], go.Figure)

    # Check the title of one figure to confirm correctness
    assert fig["Protein (g)"].layout.title.text == "Ratios for Top 4 Recipes by Protein (g)"
