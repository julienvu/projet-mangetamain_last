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
def set_global_styles():
    st.markdown(
        """
        <style>
        body {
            color: #000000; /* black text */
            font-family: 'Times New Roman', without-serif;
            font-weight: bold; /* bold */
        }
        .stApp {
            background-color: #D2B48C; /* Clear color */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.fragment
def display_explications_webapp() -> None:
    st.write(
        "**Welcome to the Mangetamain webapp,** "
        "**where we dive deep into the world of bio recipes.** "
        "**This project is based on two central themes,** "
        "**both focused on providing valuable insights** "
        "**into healthier eating and optimal nutrition.**"
    )

    st.write(
        "**The first part of the project focuses on bio recipes.** "
        "**Here, I worked on generating KPIs** "
        "**to uncover meaningful patterns and observations.** "
        "**We analyzed the number of ingredients** "
        "**in bio recipes,calculated the percentage of recipes within the original** "
        "'**Raw_recipes**' "
        "**dataset, and examined the total number of bio recipes available.** "
        "**These metrics provide a clear** "
        "**picture of the scope and richness of bio-based cooking.**"
    )

    st.write(
        "**The second theme revolves around studying the nutritional** "
        "**components of bio recipes.** "
        "**By ranking the top 4 recipes for each nutritional component,** "
        "**we can identify which dishes** "
        "**align best with specific dietary needs.** "
        "**This ranking offers practical guidance for those seeking** "
        "**recipes that support muscle development, manage blood sugar,** "
        "**or promote overall health.**"
    )

    st.write(
        "**In addition to the rankings, I created various visualizations,** "
        "**such as charts illustrating** "
        "**the ratio of proteins to sodium and proteins to carbohydrates.** "
        "**These insights are critical for** "
        "**users who want to optimize their diet to combat diabetes,** "
        "**high blood pressure,** "
        "**or strengthen muscles.** "
        "**By visualizing these ratios,** "
        "**we make it easier for users to select the right recipes for their goals.**"
    )

    st.write(
        "**To make the recommendations more practical,** "
        "**I included a table showcasing the ideal recipes tailored** "
        "**for users with specific dietary goals,** "
        "**whether it's muscle development or reducing the risk of diabetes.** "
        "**This table consolidates all the insights in an easily accessible format,** "
        "**empowering users to make informed choices.**"
    )

    st.write(
        "**The results from these analyses have been enlightening.** "
        "**The nutritional content of some recipes was higher** "
        "**than expected, offering insights in their potential health benefits.** "
        "**This exploration has also provided** "
        "**me with a deeper understanding of how bio recipes can** "
        "**contribute to healthier eating habits.**"
    )

    st.write(
        "**Through this project, I have gained valuable insights that will guide** "
        "**future work.** "
        "**in the realm of bio recipes.** "
        "**By focusing on both nutrient composition and practical dietary advice,** "
        "**I believe this webapp offers users the** "
        "**tools they need to make healthier, more informed food choices.**"
    )


@st.fragment
def display_title() -> None:
    """Displays the main title of the project"""
    st.markdown(
        "<h1 style='font-size: 36px; text-align: center;'>Welcome to Mangetamain</h1>",
        unsafe_allow_html=True,
    )


@st.fragment
def display_statistics(
    df_preprocessed: pd.DataFrame, rate_bio_recipes: float, outliers_zscore_df: int
) -> None:
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
def add_background_from_url(url: str) -> None:
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
    st.plotly_chart(fig2, key="unique_key_for_selectbox_50", use_container_width=True)


@st.fragment
def display_nutritional_analysis() -> None:
    """Displays a dropdown and chart for nutritional components analysis"""
    st.subheader("🍲 Top 4 Recipes per nutritional component (calories in Kcal)")
    selected_category = st.radio(
        "Select a nutritional component", categories, key="unique_key_for_selectbox_1"
    )
    st.plotly_chart(
        nutrition_hist[selected_category],
        key="unique_key_for_selectbox_8",
        use_container_width=True,
    )


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
    st.plotly_chart(
        nutrition_hist_ratio[selected_category],
        key="unique_key_for_selectbox_670",
        use_container_width=True,
    )


@st.fragment
def display_ideal_recipes_health() -> None:
    """Displays the ideal recipes for the health contributors ."""
    # Categories that exist in the dictionary
    data = {
        "Category": [
            "🏋️‍♂️ Ideal recipes for muscle strengthening",
            "🫀 Ideal recipes against diabetes and high blood pressure",
            "🫀 Ideal recipes against diabetes and high blood pressure",
            "🫀 Ideal recipes against diabetes and high blood pressure",
            "🫀 Ideal recipes against diabetes and high blood pressure",
        ],
        "Recipes": [
            "Jambon persille",
            "Powdered hot cocoa mix",
            "Tennessee Moonshine",
            "Jambon persille",
            "Apple core and peeling jeely",
        ],
    }

    # Dataframe creation
    df = pd.DataFrame(data)
    # Display the table
    st.dataframe(df)


@st.fragment
def clear_cache_button() -> None:
    """Empty cache"""
    if st.button("Empty cache and memory manually"):
        st.cache_data.clear()
        st.cache_resource.clear()


def main():
    background_url = (
        "https://assets.afcdn.com/imsite1/acc11_691465/"
        "acc1257x1257a871129_w450h311c1.jpg"
    )  # Image URL
    add_background_from_url(background_url)
    set_global_styles()
    display_explications_webapp()
    display_title()
    # Sidebar setup
    st.sidebar.title("**Sidebar of our food bio recipes project**")
    # Expander for cache clearing
    with st.sidebar.expander("🛠️ Advanced options", expanded=False):
        if st.checkbox("ო Clear cache", True, key="clear_cache"):
            clear_cache_button()
        if st.checkbox("🔄 Refresh Page"):
            st.query_params(reload="true")
    # Expander for general observations
    with st.sidebar.expander("📊 General observations"):
        show_general_obs = st.checkbox(
            "Bio recipes KPI", True, key="general_observations_checkbox34"
        )
        show_general_obs = st.checkbox(
            "Evolution of interactions", True, key="general_observations_checkbox4453"
        )
    # Expander for nutritional components analysis
    with st.sidebar.expander("🍏 Nutritional components"):
        show_nutritional_analysis = st.checkbox(
            "Ranking recipes based on nutritional components",
            True,
            key="nutritional_analysis_checkbox58",
        )
        show_nutritional_analysis = st.checkbox(
            "Ranking recipes based on nutritional components ratio",
            True,
            key="nutritional_analysis_checkbox_576",
        )
    # Expander for health diets
    with st.sidebar.expander("🍴 Food diets"):
        show_health_diets = st.checkbox(
            "Show food diets against diabetes and for muscle strengthening",
            True,
            key="health_diet",
        )

    # Main content
    if show_general_obs:
        st.subheader("Bio recipes KPI")
        display_statistics(df_preprocessed, rate_bio_recipes, outliers_zscore_df)
        st.subheader("Interations graph")
        display_general_observations()

    if show_nutritional_analysis:
        st.subheader("Observations of recipes regarding their nutritional components")
        display_nutritional_analysis()

        st.subheader("Observations of recipes regarding their components ratio")
        display_nutritional_analysis_ratio(context_key="nutritional_components")

    if show_health_diets:
        st.subheader("💕 The ideal recipes")
        display_ideal_recipes_health()


if __name__ == "__main__":
    main()
