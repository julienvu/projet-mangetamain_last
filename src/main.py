import streamlit as st

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
def display_title():
    """Displays the main title of the project"""
    st.write("Welcome into Mangetamain! data exploration & analysis project")


@st.fragment
def display_statistics(df_preprocessed, rate_bio_recipes, outliers_zscore_df):
    """Displays the key statistics using st.metric widgets"""
    row0_1, row0_2, row0_3 = st.columns(3)

    with row0_1:
        st.markdown(
            "<div style='margin-top: 20px;'>Bio recipes overview</div>",
            unsafe_allow_html=True,
        )
    with row0_2:
        st.markdown(
            "<div style='margin-top: 40px;'>Large community fan</div>",
            unsafe_allow_html=True,
        )
    with row0_3:
        st.markdown(
            "<div style='margin-top: 60px;'>Ingredient food</div>",
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
def display_general_aspects():
    """Displays general analysis charts"""
    st.write("The website and the database was extremely visited before 2011.")
    st.write("Instagram had an impact of the number of visitors after 2011.")
    st.plotly_chart(fig2)


@st.fragment
def display_nutritional_analysis():
    """Displays a dropdown and chart for nutritional components analysis"""
    st.title("Top 4 Recipes per nutritional component")
    selected_category = st.selectbox(
        "Select a nutritional component", categories, key="unique_key_for_selectbox_1"
    )
    st.plotly_chart(nutrition_hist[selected_category])


@st.fragment
def display_nutritional_analysis_ratio():
    """Displays a dropdown and chart for nutritional components analysis ratio."""
    # Categories that exist in the dictionary
    categories = ["Protein (g)", "Sodium (mg)", "Carbohydrates (g)"]

    # Dropdown to select a category
    selected_category = st.selectbox(
        "Select a nutritional component", categories, key="unique_key_for_selectbox_2"
    )
    st.plotly_chart(nutrition_hist_ratio[selected_category])


@st.fragment
def display_ideal_recipes_ratio_health():
    """Displaysthe ideal recipes for the health contributors ."""
    # Categories that exist in the dictionary
    st.write("Ideal recipes for muscle strengthening:")
    st.write("Powdered hot cocoa mix ")
    st.write("Jambon persille")
    st.write("Ideal recipes against diabete and high blood pressure:")
    st.write("Powdered hot cocoa mix")
    st.write("Tennessee Moonshine")


@st.fragment
def clear_cache_button():
    """Empty cache"""
    if st.button("Empty cache manually"):
        st.cache_data.clear()


def main():
    display_title()
    display_statistics(df_preprocessed, rate_bio_recipes, outliers_zscore_df)
    # Sidebar setup
    st.sidebar.title("“This is the sidebar”")
    if st.sidebar.checkbox("Clear cache", True, key="clear_cache"):
        st.subheader("Some general purpose analysis")
        display_general_aspects()
    if st.sidebar.checkbox(
        "Show general aspects", True, key="general_aspects_checkbox"
    ):
        st.subheader("Some general purpose analysis")
        display_general_aspects()
    # displaying nutritional components recipe bio
    if st.sidebar.checkbox(
        "Show analysis of nutritional components",
        True,
        key="nutritional_analysis_checkbox",
    ):
        st.subheader("Ranking of recipes regarding their components")
        display_nutritional_analysis()
        # displaying nutritional ratio recipes
        display_nutritional_analysis_ratio()
    if st.sidebar.checkbox(
        "Show food diets against diabete and for muscle strengthening",
        True,
        key="health_diet_checkbox",
    ):
        # displaying nutritional ratio recipes
        display_nutritional_analysis_ratio()
        # displaying ideal recipes for reducing diabete and muscle strenghtening
        st.subheader("The ideal recipes")
        display_ideal_recipes_ratio_health()


if __name__ == "__main__":
    main()
