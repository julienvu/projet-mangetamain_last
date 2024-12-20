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
@st.cache_data(ttl=3600)
def load_data_files():
    """
    Load data files required for the application.

    Uses the `data_loader` from `st.session_state` to load:
    1. `PP_users`: A CSV file containing user data, stored as a zipped CSV.
    2. `ingredients`: A pickled file mapping ingredients with metadata.

    Returns:
        tuple: Two pandas DataFrames:
            - `df_PP_users`: DataFrame containing user data.
            - `df_ingredients`: DataFrame mapping ingredients and their metadata.

    Notes:
        - `data_loader` must exist in `st.session_state`.
        - and include a `load_data` method.
        - Data paths are relative to the "dataset" directory.
    """
    data_loader = st.session_state.data_loader
    df_PP_users = data_loader.load_data("dataset/PP_users.csv.zip")
    df_ingredients = data_loader.load_data("dataset/ingr_map.pkl")
    return df_PP_users, df_ingredients


df_PP_users, df_ingredients = load_data_files()


@st.fragment
def set_global_styles():
    """
    Apply custom global styles to the Streamlit app using CSS.

    This function customizes:
    - Font: 'Times New Roman', bold, black text.
    - Background color: #D2B48C (tan).

    Behavior:
        - Injects CSS using `st.markdown`.
        - `unsafe_allow_html` is used to enable custom HTML and CSS.
    """
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
def display_featureengineeringsteps() -> None:
    """
    Display the steps of feature engineering in interactions and recipes data

    Explains the project's two main themes:
    1. **interactions data feature engineering steps**:
    2. **recipes data feature engineering steps**:
    Behavior:
        - Uses `st.markdown` to display formatted project details.
        - Highlights data-driven insights on bio recipes and health.
    """
    # interactions data
    st.title("Feature engineering for interactions dataset")
    feature_engineering_text_interactions = """
        **Feature Engineering steps (preprocessed_data folder in the file
        PP_interactions_mangetamain.csv) :**
        1. **Data Parsing and Cleaning**
        - **Remove Irrelevant Columns**: Dropping columns
        that are not useful for analysis
        - `review`
        - `cuisine`
        - `rating`
        - `interaction_type`
        - **Remove outliers**: using z-score method
        - **Deleting rows with duplicates**
        2. **Date-related features:**
        - Extracting day, month, year from the `date` column.

        3. **Interaction type:**
        - Interaction count: Counting the number of interactions per `recipe_id`.

        4. **User-based features:**
        - Total interactions per user: Counting how many recipes
          a user has interacted with.

        5. **Handling missing data:**
        - Filling missing values in numeric columns with NaN values.
        ---

        **Summary about the columns :**
        1. **Columns to Drop:**
        - `review`
        - `cuisine`
        - `rating`
        - `interaction_type`
        2. **Columns to Retain:**
        - `recipe_id`
        - `date`
    """
    st.markdown(feature_engineering_text_interactions)
    st.title("Feature engineering for recipes dataset")
    # Step 1: Data Parsing and Cleaning
    st.markdown(
        """
        preprocessed_data folder (PP_recipes_mangetamain.csv)
        1. Data parsing and cleaning
        - **Nutrition data**: The `nutrition` column contains a
        list of values representing
        different nutritional components. Spliting it into separate columns for
        - Calories
        - Total Fat
        - Proteins
        - Carbohydrates
        - Sugar
        - Sodium
        - Saturated Fat
        - **Ingredient IDs**: The `ingredient_ids` column stores a list of
        ingredient IDs.
        - **Tags**: Filtering the dataframe by using the `tags`
        column related to the bio keywords (substainable, eco-friendly,
        fresh, natural and so on).
        - **Remove irrelevant columns**: Dropping columns
        that are not useful for analysis.
        """
    )

    # Step 2: Feature Engineering on Nutrition Data
    st.markdown(
        """
        2. Feature Engineering on nutrition data
        - Creating new columns from the `nutrition`
        data as described above.
        - Studying the values and the international unit measures of each
        nutritional component
        """
    )

    # Step 3: Handling Ingredient IDs
    st.markdown(
        """
        3. Handling ingredient IDs
        - **Ingredient Count**: Adding a feature
        representing the total number of ingredients
        in each recipe.
        """
    )

    # Step 4: Integrating User Interaction Data
    st.markdown(
        """
        4. Integrating user interaction data
        - **Join Interaction Data**: Merging the recipe
        dataset with user interaction data to
        enrich it with features like:
            - Total interaction count per recipe.
        """
    )

    # Step 5: Handling Missing Values
    st.markdown(
        """
         5. Handling missing
         values
        - **Dropping rows/columns**: Removing rows or columns with excessive missing
        data.
        """
    )

    # Step 6: Advanced Transformations and Modeling
    st.markdown(
        """
        6. Advanced transformations and modeling
        - **Normalization/Standardization**: Scaling numerical
        features using methods like
        Min-Max scaling or Z-score normalization for better model performance.
        Deleting outliers (recipes with `minutes` column values equal
        to 0 and superior to 3600 minutes)
        """
    )
    st.markdown(
        """
        **Summary about the columns:**
        1. **Columns to Drop:**
        - `minutes`
        - `contributor_id`
        - `submitted`
        - `tags`
        - `n_steps`
        - `steps`
        - `description`
        2. **Columns to Retain:**
        - `name`
        - `id`
        - `nutrition`
        - `ingredient_ids`
        """
    )


@st.fragment
def display_explications_webapp() -> None:
    """
    Display the introduction and purpose of the web application.

    Explains the project's two main themes:
    1. **Bio Recipes Analysis**:
       - Evaluates bio recipe counts and ingredients.
       - Calculates KPIs such as ingredient variety and recipe proportions.
    2. **Nutritional Analysis**:
       - Ranks top recipes by nutritional content (e.g., proteins, carbs).
       - Provides insights for dietary goals like muscle strengthening.

    Behavior:
        - Uses `st.write` to display formatted project details.
        - Highlights data-driven insights on bio recipes and health.
    """
    st.write(
        "**Welcome to the Mangetamain webapp,** "
        "**where we dive deep into the world of bio recipes.** "
        "**This project is based on two central themes,** "
        "**both focused on providing valuable insights** "
        "**into healthier eating and optimal nutrition.**"
    )

    st.write(
        "**The first part of the project focuses on bio recipes.** "
        "**Here, I worked on generating KPI's** "
        "**to share meaningful patterns and observations.** "
        "**We analyzed the number of ingredients** "
        "**in bio recipes, calculated the percentage of recipes within the original** "
        "**raw recipes** "
        "**dataset and examined the total number of bio recipes available.** "
        "**These metrics provide a clear** "
        "**picture of the scope and richness of bio-based cooking.** "
        "**I showed other indicators about users (techniques, number of users)** "
        "**and ingredients.** "
    )

    st.write(
        "**The second theme revolves around studying the nutritional** "
        "**components of bio recipes.** "
        "**By ranking the top 4 recipes for each nutritional component,** "
        "**we can identify which dishes align best with specific dietary needs.** "
        "**This ranking provides practical guidance for those seeking** "
        "**recipes that support muscular development, control blood sugar** "
        "**or promote overall health.** "
        "**I decided to maximize the proteins quantities in the ranking.** "
        "**The recipes with the lower values are chosen** "
        "**about the other nutritional components.** "
    )

    st.write(
        "**In addition to the rankings, I created various visualizations** "
        "**such as charts illustrating** "
        "**the ratio of proteins to sodium,** "
        "**proteins to carbohydrates and the proteins to saturated fat.** "
        "**For each chart, I selected the recipe that has the highest ratio value.** "
        "**These insights are crucial for** "
        "**users who want to optimize their diet to strive against diabete,** "
        "**high blood pressure, bad cholesterol** "
        "**or strengthen muscles.** "
        "**Visualizing these ratios** "
        "**makes it easier for users to adopt the right recipes for their goals.** "
    )

    st.write(
        "**To give the efficient recommendations,** "
        "**I included a table showcasing the ideal recipes tailored** "
        "**for users with specific dietary goals. It refers to** "
        "**muscular development, reducing the risk of diabete or bad cholesterol.** "
        "**This table combines all the insights in an available format.** "
        "**It empowers users to make informed choices.**"
    )

    st.write(
        "**The results from these analyses have been enlightening.** "
        "**The nutritional content of some recipes was lower** "
        "**than expected, giving insights in their potential health benefits.** "
        "**This exploration has also provided** "
        "**me with a deeper understanding of how bio recipes can** "
        "**contribute to healthier eating habits.**"
    )

    st.write(
        "**Through this project, I have gained valuable insights that will guide** "
        "**future work.** "
        "**By focusing on both nutrient composition and practical dietary advice,** "
        "**I believe this webapp offers users the** "
        "**tools they need to make healthier, more informed food choices.**"
    )


@st.fragment
def display_title() -> None:
    """Displays the main title of the project"""
    st.markdown(
        "<h1 style='font-size: 36px; text-align: center;'>Mangetamain world</h1>",
        unsafe_allow_html=True,
    )


@st.cache_data(ttl=3600)
@st.fragment
def display_statistics(
    df_preprocessed: pd.DataFrame, rate_bio_recipes: float, outliers_zscore_df: int
) -> None:
    """
    Display key statistics using `st.metric` widgets.

    Args:
        df_preprocessed (pd.DataFrame):
            DataFrame containing preprocessed bio recipe data.
        rate_bio_recipes (float):
            Proportion of bio recipes as a percentage.
        outliers_zscore_df (int):
            Number of outliers detected using Z-score analysis.

    Behavior:
        - Metrics for total bio recipes, contributors, and ingredients.
        - Displays three-column layout for clear visualization.
        - Uses Streamlit's `st.metric` widgets for dynamic data display.

    Example:
        ```python
        display_statistics(df, 45.6, 100)
    """
    # Calculate unique techniques from df_PP_users
    num_different_techniques = df_PP_users["techniques"].nunique()
    # Section 1: Bio Recipes Overview
    st.markdown(
        """
        <div style="border: 2px solid #e0e0e0; padding: 20px; margin-bottom: 20px;">
            <h2 style="text-align: center; font-size: 32px;">Bio Recipes Overview</h2>
            <div style="margin-top: 10px; font-size: 27px;">
                <p>Total bio recipes:</p>
                <b style="font-size: 26px;color: green;">{}</b>
            </div>
            <div style="margin-top: 10px; font-size: 27px;">
                <p>Bio recipes proportion (%):</p>
                <b style="font-size: 26px;color: green;">{:.2f}%</b>
            </div>
            <div style="margin-top: 10px; font-size: 27px;">
                <p>Outliers detected:</p>
                <b style="font-size: 26px;color: green;">{}</b>
            </div>
        </div>
        """.format(
            f"{df_preprocessed.shape[0]:,}".replace(",", " "),
            rate_bio_recipes,
            (
                len(outliers_zscore_df)
                if isinstance(outliers_zscore_df, (list, pd.DataFrame))
                else outliers_zscore_df
            ),
        ),
        unsafe_allow_html=True,
    )

    # Section 2: Community Contributions
    st.markdown(
        """
        <div style="border: 2px solid #e0e0e0; padding: 20px; margin-bottom: 20px;">
            <h2 style="text-align: center; font-size: 32px;">Community Insights</h2>
            <div style="margin-top: 10px; font-size: 27px;">
                <p>Total users:</p>
                <b style="font-size: 26px;color: #ff69b4;">{}</b>
            </div>
            <div style="margin-top: 10px; font-size: 27px;">
                <p>New users (last month):</p>
                <b style="font-size: 26px;color: #ff69b4;">452</b>
            </div>
            <div style="margin-top: 10px; font-size: 27px;">
                <p>Number of different techniques:</p>
                <b style="font-size: 26px;color: #ff69b4;">{}</b>
            </div>
        </div>
        """.format(
            f"{df_PP_users.shape[0]:,}".replace(",", " "),
            f"{num_different_techniques:,}".replace(",", " "),
        ),
        unsafe_allow_html=True,
    )

    # Section 3: Ingredient Insights
    st.markdown(
        """
        <div style="border: 2px solid #e0e0e0; padding: 20px;">
            <h2 style="text-align: center; font-size: 32px;">Ingredient Insights</h2>
            <div style="margin-top: 10px; font-size: 27px;">
                <p>Unique ingredients:</p>
                <b style="font-size: 26px;color: orange;">{}</b>
            </div>
        </div>
        """.format(
            f"{df_ingredients.shape[0]:,}".replace(",", " "),
        ),
        unsafe_allow_html=True,
    )


@st.fragment
def add_background_from_url(url: str) -> None:
    """Adds a background image to the Streamlit app using CSS.
    This function embeds custom CSS to set a background image for the entire
    Streamlit app by applying the style to the `.stApp` class. The image is
    sourced from the specified URL and styled to provide a visually appealing
    full-screen background.

    Args:
        url (str):
            A direct URL pointing to the image file (e.g., PNG, JPG, or GIF)
            that will be used as the background.

    Behavior:
        - The background image is resized to cover the entire viewport.
        - The image is centered both horizontally and vertically.
        - The image does not repeat and remains fixed during scrolling.

    Example:
        ```python
        import streamlit as st

        add_background_from_url("https://example.com/background.jpg")
        st.title("Welcome to My Streamlit App!")
        ```
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
    st.plotly_chart(fig2, key="unique_key_for_selectbox_50", use_container_width=True)


@st.fragment
def display_nutritional_analysis() -> None:
    """Displays a dropdown and chart for nutritional components analysis
    Displays a dropdown and chart for nutritional component analysis.

    This function provides an interface for users to select a nutritional
    component (e.g., calories) via a radio button and displays a histogram
    for the top four recipes in the selected category.

    Behavior:
        - Displays a subheader for the analysis.
        - Allows selection of a nutritional component through a radio button.
        - Renders an interactive Plotly chart for the selected component.

    Example:
        ```python
        display_nutritional_analysis()
    """
    st.subheader("🥥 Top 4 Recipes per nutritional component (calories in Kcal)")
    # Help button with an interactive display
    if st.button("ℹ️ Current Daily Value (DV) guide"):
        st.markdown(
            """
            <div style='padding: 20px; background-color: #000000; border-radius: 10px;'>
                <h4 style='color: #ff69b4;'>Nutritional components</h4>
                <ul style="list-style-type: square; color: #ff69b4;">
                    <li><strong>Calories:</strong> 2,000 Kcal</li>
                    <li><strong>Total fat:</strong> 78 g</li>
                    <li><strong>Sugar:</strong> 50 g</li>
                    <li><strong>Sodium:</strong> 2,300 mg</li>
                    <li><strong>Protein:</strong> 50 g</li>
                    <li><strong>Saturated fat:</strong> 20 g</li>
                    <li><strong>Carbohydrates:</strong> 275 g</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    # Layout with columns: 85% for the graph, 15% for the form
    col1, col2 = st.columns([8.0, 2.0])

    with col1:
        # Custom HTML to wrap the radio button inside a div with class for styling
        selected_category = st.radio(
            "🔥 Select a nutritional component",
            categories,
            key="unique_key_for_selectbox_1",
        )
        # Add border and margin around the chart to separate it from the radio buttons
        st.markdown(
            """
            <style>
                .chart-container {
                    margin-top: 20px;  /* Space between radio buttons and the chart */
                    border: 2px solid #e0e0e0;
                    padding: 15px;
                    border-radius: 8px;
                    background-color: #f9f9f9;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Plot the selected nutritional analysis chart
        st.plotly_chart(
            nutrition_hist[selected_category],
            key="unique_key_for_selectbox_8",
            use_container_width=True,
        )
    with col2:
        # Add margin to align the form vertically with the graph
        # Apply custom styling to the form container
        st.markdown(
            """
            <style>
                .form-container {
                    margin-top: 20px;
                    padding: 15px;
                    border: 2px solid #ff69b4;
                    border-radius: 10px;
                    background-color: #ff69b4;
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                }
                .stSelectbox, .stNumberInput {
                    margin-bottom: 15px;
                }
                .stButton>button {
                    background-color: #2E8B57;
                    color: green;
                    border-radius: 5px;
                    border: none;
                    padding: 8px 20px;
                    cursor: pointer;
                }
                .stButton>button:hover {
                    background-color: #ff69b4;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        # Add form within styled container
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        # CDV Conversion Form
        st.markdown("% Daily Value ---> g/mg")
        with st.form("dv_conversion_form"):
            # Select component for conversion
            component = st.selectbox(
                "Nutritional component:",
                [
                    "Total fat",
                    "Sugar",
                    "Sodium",
                    "Protein",
                    "Saturated fat",
                    "Carbohydrates",
                ],
            )

            # Input for %CDV
            dv = st.number_input(
                f"% Daily Value for {component}:",
                min_value=0.0,
                max_value=100.0,
                step=1.0,
            )

            # Submit button for the form
            submitted = st.form_submit_button("Convert")

            if submitted:
                # Daily values for each component
                daily_values = {
                    "Total fat": 78,
                    "Sugar": 50,
                    "Sodium": 2300,
                    "Protein": 50,
                    "Saturated fat": 20,
                    "Carbohydrates": 275,
                }

                if component in daily_values:
                    # Perform conversion based on daily value and %CDV input
                    converted_value = (dv * daily_values[component]) / 100
                    unit = "mg" if component == "Sodium" else "g"

                    # Display conversion result
                    st.success(f"{converted_value:.2f} {unit}.")


@st.fragment
def display_nutritional_analysis_ratio(context_key: str = "default") -> None:
    """Displays a dropdown and chart for nutritional components analysis ratio.
    This function enables users to analyze ratios for different nutritional
    components by selecting a category. The chart adapts based on the selected
    category and a context-specific key to ensure uniqueness in Streamlit's state.

    Args:
        context_key (str):
            A unique identifier for differentiating between similar widgets in
            different contexts. Defaults to 'default'.

    Behavior:
        - Provides a radio button for selecting nutritional categories.
        - Displays an interactive Plotly chart based on the selected category.

    Example:
        ```python
        display_nutritional_analysis_ratio(context_key="unique_context")
    """
    # Categories that exist in the dictionary
    categories = [
        "Protein (g)",
        "Sodium (mg)",
        "Saturated Fat (g)",
        "Carbohydrates (g)",
    ]

    # Add border and style to the radio buttons container
    selected_category = st.radio(
        "Select a nutritional component",
        categories,
        key=f"selectbox_{context_key}",  # Dynamically generate a unique key
    )
    # Add border and margin around the chart to separate it from the radio buttons
    st.markdown(
        """
        <style>
            .chart-container {
                margin-top: 20px;  /* Space between radio buttons and the chart */
                border: 2px solid #e0e0e0;
                padding: 15px;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Plot the selected nutritional analysis ratio chart
    st.plotly_chart(
        nutrition_hist_ratio[selected_category],
        key="unique_key_for_selectbox_670",
        use_container_width=True,
    )


@st.fragment
def display_ideal_recipes_health() -> None:
    """Displays the ideal recipes for the health contributors .
    This function creates and displays a dataframe that lists ideal recipes
    for various health goals like muscle strengthening and managing
    diabete or high blood pressure.

    Behavior:
        - Constructs a pandas DataFrame with health categories and recipes.
        - Displays the dataframe as an interactive table in Streamlit.

    Example:
        ```python
        display_ideal_recipes_health()
    """
    # Categories that exist in the dictionary
    data = {
        "Category": [
            "🏋️‍♂️ Muscle strengthening and obesity",
            "🏋️‍♂️ Muscle strengthening and obesity",
            "🫀 Diabete and high blood pressure",
            "🫀 Diabete and high blood pressure",
            "🫀 Diabete and high blood pressure",
            "🫀 Diabete and high blood pressure",
            "🥓 Bad cholesterol",
            "🥓 Bad cholesterol",
            "🥓 Bad cholesterol",
        ],
        "🍉 Recipes (selecting the highest ratio value and ideally higher than 1.0)": [
            "lighter pistachio pudding salad",
            "basic baked fish easy dressing",
            "creamy cucumber bites",
            "lighter pistachio pudding salad",
            "light and fluffy vegan lemon scones",
            "basic baked fish easy dressing",
            "easy cinnamon sugar muffins",
            "libbie s corn for freezing",
            "basic baked fish easy dressing",
        ],
    }

    # Dataframe creation
    df = pd.DataFrame(data)
    # Style the dataframe with Pandas Styler (green text for all content)
    styled_df = df.style.set_properties(
        **{
            "color": "white",  # white  text for the content
        }
    ).set_table_styles(
        [{"selector": "th", "props": [("color", "#006400")]}]  # Dark green for headers
    )
    # Display the styled dataframe
    st.write(styled_df.hide(axis="index").to_html(), unsafe_allow_html=True)


@st.fragment
def clear_cache_button() -> None:
    """Empty cache
    This function renders a button that allows users to clear both data
    and resource caches in Streamlit. This is useful for refreshing data
    or freeing up memory during app development and testing.

    Behavior:
        - Clears the `st.cache_data` and `st.cache_resource`

    Example:
        ```python
        clear_cache_button()
    """
    if st.button("Empty cache and refresh"):
        # Vider le cache de Streamlit
        st.cache_data.clear()
        st.cache_resource.clear()

        # Rafraîchir la page sans cache en ajoutant un paramètre unique
        st.markdown(
            """
            <script>
            window.location.href = window.location.href.split('?')[0] + '?nocache=';
            </script>
            """,
            unsafe_allow_html=True,
        )


def main():
    st.markdown(
        """<style>
            header[data-testid="stHeader"] {
                display: none;
            }
            footer {
                display: none;
            }
            [data-testid="stSidebar"] {
                background-color: #2E8B57;  /* Vert foncé */
                padding: 20px;
            }
            </style>
            """,
        unsafe_allow_html=True,
    )
    background_url = (
        "https://assets.afcdn.com/imsite1/acc11_691465/"
        "acc1257x1257a871129_w450h311c1.jpg"
    )  # Image URL
    add_background_from_url(background_url)
    # set_global_styles()
    display_title()
    # Sidebar setup
    st.markdown(
        """
        <style>
            /* Sidebar color */
            [data-testid="stSidebar"] {
                background-color: #2E8B57,
                padding: 0;
                margin: 0;
                overflow: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    clear_cache_button()
    # Expander for general observations
    with st.sidebar.expander("🍒 Storytelling and feature engineering"):
        show_storytelling = st.checkbox(
            "Storytelling for my webapp",
            True,
            key="storytelling_checkbox3490",
        )
        show_feature_engineering = st.checkbox(
            "Feature engineering", True, key="feature_engineering_checkbox4443"
        )
    # Expander for general observations
    with st.sidebar.expander("📊 General observations"):
        show_general_obs = st.checkbox(
            "Key numbers for recipes, ingredients and community",
            True,
            key="general_observations_checkbox34",
        )
        show_inter_obs = st.checkbox(
            "Interactions", True, key="general_observations_checkbox4453"
        )
    # Expander for nutritional components analysis
    with st.sidebar.expander("🥒 Nutritional components findings"):
        show_nutritional_analysis = st.checkbox(
            "Recipes ranking/nutritional component",
            True,
            key="nutritional_analysis_checkbox58",
        )
        show_nutritional_analysis_1 = st.checkbox(
            "Recipes ranking/nutritional component ratio",
            True,
            key="nutritional_analysis_checkbox_576",
        )
    # Expander for health diets
    with st.sidebar.expander("🍽️ Food diets"):
        show_health_diets = st.checkbox(
            "Diet plans: diabete, obesity, muscle strenghtening & bad cholesterol",
            True,
            key="health_diet",
        )
    # Expander for cache clearing
    with st.sidebar.expander("🛠️ Advanced options", expanded=False):
        if st.checkbox("🔄 Refresh Page", key="refresh_page_button"):
            st.markdown(
                """
                <script>
                window.location.reload();
                </script>
                """,
                unsafe_allow_html=True,
            )
    # storytelling button
    if show_storytelling:
        display_explications_webapp()
    # feature engineering button
    if show_feature_engineering:
        display_featureengineeringsteps()
    # Main content
    if show_general_obs:
        st.subheader("Key numbers for recipes")
        display_statistics(df_preprocessed, rate_bio_recipes, outliers_zscore_df)

    if show_inter_obs:
        st.subheader("👨🏻‍💻 Interactions graph")
        display_general_observations()

    if show_nutritional_analysis:
        st.subheader(
            "🎯 Observations of recipes regarding their nutritional components"
        )
        display_nutritional_analysis()

    if show_nutritional_analysis_1:
        st.subheader("📈 Observations of recipes regarding their components ratio")
        display_nutritional_analysis_ratio(context_key="nutritional_components")

    if show_health_diets:
        st.subheader("ﮩـﮩﮩ٨ـ🫀ﮩ٨ـﮩﮩ٨ـ Top recipes for optimal health")
        display_ideal_recipes_health()


if __name__ == "__main__":
    main()
