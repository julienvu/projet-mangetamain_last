import pytest
import pandas as pd
import plotly.graph_objects as go
from src.data_loader import DataLoader
import plotly.express as px
from src.visualisation import graphs


@pytest.fixture
def interactions_data():
    # Simulate data loading by dataloader
    data_loader = DataLoader()
    interactions = data_loader.load_data("dataset/RAW_interactions.csv.xz")
    return interactions

@pytest.fixture
def interactions_preprocessed_data():
    # Simulate data loading by dataloader 
    data_loader = DataLoader()
    interactions_preprocessed = data_loader.load_data(
    "preprocessed_data/PP_interactions_mangetamain.csv")
    return interactions_preprocessed

def test_interactions_loading(interactions_data):
    """
    Test the data loading process for the `interactions_data` DataFrame.

    Purpose:
    Ensure that the data loaded from the `RAW_interactions.csv.xz` file is a Pandas DataFrame
    and contains the expected columns necessary for further analysis.

    Parameters:
    - interactions_data (pd.DataFrame): A fixture that returns the raw interactions data.

    Steps:
    1. Verify that `interactions_data` is an instance of `pd.DataFrame`.
    2. Check for the existence of key columns such as 'rating', 'date', and 'recipe_id'.

    Expected Results:
    - The data should be loaded into a DataFrame.
    - Columns 'rating', 'date', and 'recipe_id' must exist in the DataFrame.

    Assertions:
    - `assert isinstance(interactions_data, pd.DataFrame)` ensures the data is a DataFrame.
    - `assert 'rating' in interactions_data.columns` ensures the 'rating' column is present.
    - `assert 'date' in interactions_data.columns` ensures the 'date' column is present.
    - `assert 'recipe_id' in interactions_data.columns` ensures the 'recipe_id' column is present.
    """
    assert isinstance(
        interactions_data, pd.DataFrame
    ), "Les données ne sont pas un DataFrame."
    # Check if the columns of the dataset exist
    assert "rating" in interactions_data.columns, "La colonne 'rating' est manquante."
    assert "date" in interactions_data.columns, "La colonne 'date' est manquante."
    assert (
        "recipe_id" in interactions_data.columns
    ), "La colonne 'recipe_id' est manquante."

def test_interactions_loading(interactions_preprocessed_data):
    """
    Test the data loading process for the `interactions_data` DataFrame.

    Purpose:
    Ensure that the data loaded from the `RAW_interactions.csv.xz` file is a Pandas DataFrame
    and contains the expected columns necessary for further analysis.

    Parameters:
    - interactions_data (pd.DataFrame): A fixture that returns the raw interactions data.

    Steps:
    1. Verify that `interactions_data` is an instance of `pd.DataFrame`.
    2. Check for the existence of key columns such as 'rating', 'date', and 'recipe_id'.

    Expected Results:
    - The data should be loaded into a DataFrame.
    - Columns 'rating', 'date', and 'recipe_id' must exist in the DataFrame.

    Assertions:
    - `assert isinstance(interactions_data, pd.DataFrame)` ensures the data is a DataFrame.
    - `assert 'rating' in interactions_data.columns` ensures the 'rating' column is present.
    - `assert 'date' in interactions_data.columns` ensures the 'date' column is present.
    - `assert 'recipe_id' in interactions_data.columns` ensures the 'recipe_id' column is present.
    """
    # Check if date is the processed data
    assert "date" in interactions_preprocessed_data.columns, "La colonne 'date' est manquante."
    assert (
        "recipe_id" in interactions_preprocessed_data.columns
    ), "La colonne 'recipe_id' est manquante."

def test_ratio_of_ratings(interactions_data):
    """
    Test the calculation of rating ratios from the `interactions_data` DataFrame.

    Purpose:
    Validate the computation of rating counts and their ratios to ensure accurate aggregation of data.

    Parameters:
    - interactions_data (pd.DataFrame): A fixture that returns the raw interactions data.

    Steps:
    1. Calculate the count of each rating using `value_counts()`.
    2. Compute the ratio of each rating relative to the total number of ratings.
    3. Verify that the resulting DataFrame contains the 'count' and 'ratio' columns.
    4. Ensure that the sum of all counts equals the total number of rows in `interactions_data`.

    Expected Results:
    - A DataFrame containing the 'count' and 'ratio' columns.
    - The total count should match the number of interactions in the dataset.

    Assertions:
    - `assert 'count' in ratio_of_ratings.columns` ensures the 'count' column is present.
    - `assert 'ratio' in ratio_of_ratings.columns` ensures the 'ratio' column is present.
    - `assert ratio_of_ratings['count'].sum() == interactions_data.shape[0]` ensures accuracy.
    """
    ratio_of_ratings = pd.DataFrame(interactions_data.rating.value_counts())
    ratio_of_ratings.columns = ["count"]
    ratio_of_ratings["ratio"] = (
        ratio_of_ratings["count"] / ratio_of_ratings["count"].sum()
    )

    # Check dataset has count and ratio columns
    assert "count" in ratio_of_ratings.columns, "La colonne 'count' est manquante."
    assert "ratio" in ratio_of_ratings.columns, "La colonne 'ratio' est manquante."
    assert (
        ratio_of_ratings["count"].sum() == interactions_data.shape[0]
    ), "La somme des 'count' ne correspond pas au nombre total d'interactions."

def test_pie_chart_creation(interactions_data):
    """
    Test the creation of a pie chart for rating ratios using Plotly.

    Purpose:
    Ensure that the `px.pie` function correctly generates a pie chart to visualize the distribution of ratings.

    Parameters:
    - interactions_data (pd.DataFrame): A fixture that returns the raw interactions data.

    Steps:
    1. Create a DataFrame with the counts and ratios of each rating.
    2. Use Plotly Express (`px.pie`) to generate a pie chart visualizing the data.
    3. Check that the resulting object is a valid Plotly `go.Figure`.

    Expected Results:
    - A Plotly `go.Figure` object representing the pie chart.

    Assertions:
    - `assert isinstance(fig1, go.Figure)` ensures the pie chart is a valid Plotly figure.
    """
    # Create dataframe
    ratio_of_ratings = pd.DataFrame(interactions_data.rating.value_counts())
    ratio_of_ratings.columns = ["count"]
    ratio_of_ratings["ratio"] = (
        ratio_of_ratings["count"] / ratio_of_ratings["count"].sum()
    )

    # Create pie chart
    fig1 = px.pie(
        ratio_of_ratings,
        names=ratio_of_ratings.index,
        values="count",
        title="Ratio of ratings in the dataset",
        color=ratio_of_ratings.index,
        color_discrete_sequence=px.colors.sequential.Blues[::-1],
    )

    # Check if the graph is figure object
    assert isinstance(
        fig1, go.Figure
    ), "Le graphique n'est pas un objet de type Figure."

def test_histogram_creation(interactions_preprocessed_data):
    """
    Test the creation of a histogram to visualize interaction evolution over time.

    Purpose:
    Verify that the `px.histogram` function correctly generates a histogram representing
    the frequency of interactions over time.

    Parameters:
    - interactions_preprocessed_data (pd.DataFrame): A fixture that returns preprocessed interactions data.

    Steps:
    1. Generate a histogram using the `date` column with `px.histogram`.
    2. Ensure the returned object is a Plotly `go.Figure`.
    3. Validate that the title of the histogram matches the expected value.

    Expected Results:
    - A valid Plotly histogram figure.
    - The title should be "Evolution of interactions".

    Assertions:
    - `assert isinstance(fig2, go.Figure)` ensures the object is a valid figure.
    - `assert fig2.layout.title.text == "Evolution of interactions"` checks the title.
    """
    # Create an histogram
    fig2 = px.histogram(interactions_preprocessed_data.date, title="Evolution of interactions")

    # Check if the graph is a figure instance
    assert isinstance(
        fig2, go.Figure
    ), "Le graphique n'est pas un objet de type Figure."

    # Check if the title is correct
    assert (
        fig2.layout.title.text == "Evolution of interactions"
    ), "Le titre de l'histogramme n'est pas correct."

def test_scatter_plot_creation(interactions_preprocessed_data):
    """
    Test the creation of a violin plot to visualize recipe popularity.

    Purpose:
    Ensure that a violin plot is generated using the `px.violin` function to display
    the distribution of recipe interaction counts.

    Parameters:
    - interactions_preprocessed_data (pd.DataFrame): A fixture that returns preprocessed interactions data.

    Steps:
    1. Calculate the value counts for `recipe_id`.
    2. Create a violin plot using `px.violin`.
    3. Verify the resulting object is a valid Plotly `go.Figure`.
    4. Ensure the title is set correctly.

    Expected Results:
    - A valid Plotly `go.Figure` object representing the violin plot.
    - The title should be "Too popular to be serious".

    Assertions:
    - `assert isinstance(fig3, go.Figure)` ensures the object is a valid Plotly figure.
    - `assert fig3.layout.title.text == "Too popular to be serious"` checks the title.
    """
    # Create scatter plot
    fig3 = px.violin(
        interactions_preprocessed_data.recipe_id.value_counts(), title="Too popular to be serious"
    )

    # Check if the graph is figure object
    assert isinstance(
        fig3, go.Figure
    ), "Le graphique n'est pas un objet de type Figure."

    # Check if the title is correct
    assert (
        fig3.layout.title.text == "Too popular to be serious"
    ), "Le titre du scatter plot n'est pas correct."

def test_annotations_in_figures(interactions_preprocessed_data):
    """
    Test the addition of annotations to a histogram figure.

    Purpose:
    Ensure that annotations are correctly added to a histogram using Plotly's `add_annotation` method.

    Parameters:
    - interactions_preprocessed_data (pd.DataFrame): A fixture that returns preprocessed interactions data.

    Steps:
    1. Create a histogram using `px.histogram`.
    2. Add an annotation with specific parameters (text, position, formatting).
    3. Verify that the annotation is correctly added.
    4. Check that the annotation's text matches the expected value.

    Expected Results:
    - A valid Plotly figure with the specified annotation.

    Assertions:
    - `assert len(fig2.layout.annotations) == 1` ensures only one annotation is added.
    - `assert fig2.layout.annotations[0].text == "Instagram"` verifies the annotation text.
    """
    # Create an histogram
    fig2 = px.histogram(interactions_preprocessed_data.date, title="Evolution of interactions")
    fig2.add_annotation(
        text="Instagram",
        x="2012-01-31",
        y=6000,
        showarrow=False,
        font=dict(size=15, color="black"),
        bgcolor="rgba(255, 255, 255, 0.7)",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
    )

    # Check if annotation
    assert (
        len(fig2.layout.annotations) == 1
    ), "L'annotation n'a pas été ajoutée correctement."
    assert (
        fig2.layout.annotations[0].text == "Instagram"
    ), "Le texte de l'annotation n'est pas correct."
