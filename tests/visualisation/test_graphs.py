import pytest
import pandas as pd
import plotly.graph_objects as go
from src.data_loader import DataLoader
import plotly.express as px
from src.visualisation import graphs


@pytest.fixture
def interactions_preprocessed_data():
    # Simulate data loading by dataloader 
    data_loader = DataLoader()
    interactions_preprocessed = data_loader.load_data(
    "preprocessed_data/PP_interactions_mangetamain.csv")
    return interactions_preprocessed

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
