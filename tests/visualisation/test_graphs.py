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
    # Check if data is dataframe
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
    # Check if date is the processed data
    assert "date" in interactions_preprocessed_data.columns, "La colonne 'date' est manquante."
    assert (
        "recipe_id" in interactions_preprocessed_data.columns
    ), "La colonne 'recipe_id' est manquante."

def test_ratio_of_ratings(interactions_data):
    # Calculate ratio ratings
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
