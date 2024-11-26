import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
from data_loader import DataLoader
from log_config import setup_logging
from utils import (
    df_preprocessed,
    rate_bio_recipes,
    outliers_zscore_df,
)
from visualisation.graphs import fig2
from visualisation.graphs_nutrition import (
    categories,
    nutrition_hist,
    nutrition_hist_ratio,
)

# Initialize logging and set page configuration
setup_logging()
# Use session state to avoid reloading data multiple times
if "data_loader" not in st.session_state:
    st.session_state.data_loader = DataLoader()


# Load data files once using caching
@st.fragment
def load_data_files():
    data_loader = st.session_state.data_loader
    df_PP_users = data_loader.load_data("dataset/PP_users.csv.zip")
    df_ingredients = data_loader.load_data("dataset/ingr_map.pkl")
    return df_PP_users, df_ingredients


df_PP_users, df_ingredients = load_data_files()


@st.fragment
def display_title() -> None:
    """Displays the main title of the project"""
    st.markdown(
        "<h1 style='font-size: 36px; text-align: center;'>Welcome to Mangetamain</h1>",
        unsafe_allow_html=True,
    )


@st.fragment
def display_statistics(df_preprocessed, rate_bio_recipes, outliers_zscore_df) -> None:
    """Displays the key statistics using st.metric widgets"""
    row0_1, row0_2, row0_3 = st.columns(3)

    with row0_1:
        st.markdown(
            "<div style='margin-top: 20px;font-size: 24px;'>Bio recipes overview</div>",
            unsafe_allow_html=True,
        )
    with row0_2:
        st.markdown(
            "<div style='margin-top: 20px;font-size: 24px;'>Large community fan</div>",
            unsafe_allow_html=True,
        )
    with row0_3:
        st.markdown(
            "<div style='margin-top: 20px;font-size: 24px;'>Ingredient food</div>",
            unsafe_allow_html=True,
        )

    row1_1, row1_2, row1_3 = st.columns(3)

    with row1_1:
        st.metric(
            label="Bio recipes",
            value=f"{df_preprocessed.shape[0]:,}".replace(",", " "),
            help="Number of bio recipes after pre-processing step",
        )
        st.metric("Bio recipes proportion (%)", f"{rate_bio_recipes:.2f}%")
        st.metric(
            label="Outliers",
            value=f"{len(outliers_zscore_df)}",
            help="Outliers count in bio recipes",
        )

    with row1_2:
        st.metric(
            label="Number of contributors",
            value=f"{df_PP_users.shape[0]:,}".replace(",", " "),
            help="Contributors who where registrered",
        )

    with row1_3:
        st.metric(
            label="Ingredients",
            value=f"{df_ingredients.shape[0]:,}".replace(",", " "),
            help="Number of different ingredients",
        )


@st.fragment
def add_background_from_url(url) -> None:
    """Adds a background image to the Streamlit app using CSS.
    args: url with text
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.fragment
def display_general_observations() -> None:
    """Displays general analysis charts"""
    st.write("🌟 The website and the database was extremely visited before 2011.")
    st.write("Instagram had an impact of the number of visitors after 2011.")
    st.plotly_chart(fig2)


@st.fragment
def display_nutritional_analysis() -> None:
    """Displays a dropdown and chart for nutritional components analysis"""
    st.subheader("🍲 Top 4 Recipes per nutritional component")
    selected_category = st.radio(
        "Select a nutritional component", categories, key="unique_key_for_selectbox_1"
    )
    st.plotly_chart(nutrition_hist[selected_category], key="unique_key_for_selectbox_8")


@st.fragment
def display_nutritional_analysis_ratio(context_key: str = "default") -> None:
    """Displays a dropdown and chart for nutritional components analysis ratio."""
    # Categories that exist in the dictionary
    categories = ["Protein (g)", "Sodium (mg)", "Carbohydrates (g)"]

    # Dropdown to select a category with a context-specific unique key
    selected_category = st.radio(
        "Select a nutritional component",
        categories,
        key=f"selectbox_{context_key}",  # Dynamically generate a unique key
    )
    st.plotly_chart(nutrition_hist_ratio[selected_category])


@st.fragment
def display_ideal_recipes_ratio_health() -> None:
    """Displays the ideal recipes for the health contributors ."""
    # Categories that exist in the dictionary
    data = {
        "Category": [
            "🏋️‍♂️ Ideal recipes for muscle strengthening",
            "🏋️‍♂️ Ideal recipes for muscle strengthening",
            "🫀 Ideal recipes against diabetes and high blood pressure",
            "🫀 Ideal recipes against diabetes and high blood pressure",
            "🫀 Ideal recipes against diabetes and high blood pressure",
            "🫀 Ideal recipes against diabetes and high blood pressure",
        ],
        "Recipes": [
            "Powdered hot cocoa mix",
            "Jambon persille",
            "Powdered hot cocoa mix",
            "Tennessee Moonshine",
            "Polish dill pickles made in a crock",
            "Roasted pepper salt blend",
        ],
    }

    # Dataframe creation
    df = pd.DataFrame(data)
    # Display the table
    st.dataframe(df)


@st.fragment
def clear_cache_button() -> None:
    """Empty cache"""
    if st.button("Empty cache manually"):
        st.cache_data.clear()


def main():
    background_url = (
        "https://www.passionamerique.com/wp-content/uploads/2021/"
        "02/table-thanksgiving-dinde.jpg"
    )  # Image URL
    add_background_from_url(background_url)
    display_title()
    display_statistics(df_preprocessed, rate_bio_recipes, outliers_zscore_df)
    # Sidebar setup
    st.sidebar.title("**Sidebar of our food bio recipes project**")
    if st.sidebar.checkbox("ო Clear cache", True, key="clear_cache"):
        clear_cache_button()
    if st.sidebar.checkbox(
        "📊 Show general observations", True, key="general_observations_checkbox"
    ):
        st.subheader("Some general purpose analysis")
        display_general_observations()
    # displaying nutritional components recipe bio
    if st.sidebar.checkbox(
        "🍏 Show analysis of nutritional components",
        True,
        key="nutritional_analysis_checkbox",
    ):
        st.subheader("Ranking of recipes regarding their components")
        display_nutritional_analysis()
        # displaying nutritional ratio recipes
        display_nutritional_analysis_ratio(context_key="nutritional_components")
    if st.sidebar.checkbox(
        "🍴 Show food diets against diabete and for muscle strengthening",
        True,
        key="health_diet",
    ):
        # displaying ideal recipes for reducing diabete and muscle strenghtening
        st.subheader("💕 The ideal recipes")
        display_ideal_recipes_ratio_health()


if __name__ == "__main__":
    main()
