from nutrition_stats import combined_df
import plotly.express as px
import pandas as pd


def plot_top_4_recipes_by_nutrition(
    combined_df: pd.DataFrame, categories: list
) -> dict:
    """
    Creates a plot for each nutritional category.
    Returns a dictionary with a Plotly figure for each category.
    Args:
        combined_df (pd.DataFrame): DataFrame containing recipe names.
        and their nutritional values.
        categories (list): List of nutritional components to be plotted.
    Returns:
        dict: A dictionary where keys are nutritional categories.
        and values are Plotly figures.
    """
    figures = {}
    for category in categories:
        # Sort recipes depending on the category
        top_4_recipes = combined_df.sort_values(by=category, ascending=False).head(4)

        fig = px.bar(
            top_4_recipes,
            x="name",
            y=category,
            title=f"Top 4 Recipes by {category}",
            labels={"name": "Recipe Name", category: category},
            color_discrete_sequence=["#1f77b4"],
        )

        # Storage the figure in the dictionnary
        figures[category] = fig
    return figures


def nutrition_bar_ratio_sodium_proteins(
    combined_df: pd.DataFrame, categories: list
) -> dict:
    """
    Creates a plot for 3 categories with the ratios
    Returns a dictionary with a Plotly figure for each category.
    Args:
        combined_df (pd.DataFrame): DataFrame containing recipe names.
        and their nutritional values.
        categories (list): List of nutritional components to be plotted.
    Returns:
        dict: A dictionary where keys are nutritional categories.
        and values are Plotly figures and the ratios
    """
    # Filter the relevant categories
    categories = ["Protein (g)", "Sodium (mg)", "Carbohydrates (g)"]
    figures = {}
    for category in categories:
        # Sort recipes depending on the category
        top_4_recipes = combined_df.sort_values(by=category, ascending=False).head(4)

        # Calculate the Protein/Carbohydrate Ratio
        top_4_recipes["Protein_Carb_Ratio"] = (
            top_4_recipes["Protein (g)"] / top_4_recipes["Carbohydrates (g)"]
        )

        # Calculate the Protein/Sodium Ratio
        top_4_recipes["Protein_Sodium_Ratio"] = top_4_recipes["Protein (g)"] / (
            top_4_recipes["Sodium (mg)"] * 0.001
        )  # Convert Sodium to grams

        # Reshape data to have both ratios as columns for grouped bar plot
        top_4_recipes_long = top_4_recipes.melt(
            id_vars=["name"],
            value_vars=["Protein_Carb_Ratio", "Protein_Sodium_Ratio"],
            var_name="Ratio Type",
            value_name="Ratio Value",
        )

        # Create a grouped bar chart
        fig2 = px.bar(
            top_4_recipes_long,
            x="name",  # Recipe names on the x-axis
            y="Ratio Value",  # Values of the ratios on the y-axis
            color="Ratio Type",  # Color based on the two ratio types
            title=f"Ratios for Top 4 Recipes by {category}",
            labels={
                "name": "Recipe Name",
                "Ratio Value": "Ratio Value",
                "Ratio Type": "Ratio Type",
            },  # Axis labels and legend title
            barmode="group",  # Group bars for each recipe (side-by-side)
            template="plotly_white",  # Clean white background for readability
        )

        # Add a reference line for a balanced ratio (optional)
        fig2.add_hline(
            y=1.0,  # Balanced ratio line
            line_dash="dot",
            annotation_text="Balanced Ratio (1.0)",
            annotation_position="bottom right",
        )
        # Store the figure in the dictionary
        figures[category] = fig2
    return figures


categories = [
    "Calories",
    "Total Fat (g)",
    "Sugar (g)",
    "Sodium (mg)",
    "Protein (g)",
    "Saturated Fat (g)",
    "Carbohydrates (g)",
]


# Generate graphs
nutrition_hist = plot_top_4_recipes_by_nutrition(combined_df, categories)
nutrition_hist_ratio = nutrition_bar_ratio_sodium_proteins(combined_df, categories)
