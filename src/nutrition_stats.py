from utils import df_preprocessed
import ast
import pandas as pd


def parse_nutrition(nutrition_str):
    """
    Parses a string representation of nutritional data into a list of floats.
    The input string typically represents a list-like format.
    with 7 nutritional values,
    and this function extracts those values into a Python list.

    If the input string cannot be parsed correctly.
    (e.g., due to syntax errors or invalid format).
    the function returns a list with seven `None` values.
    which ensures that all returned lists.
    have a consistent length, even in case of parsing failures.

    Args:
        nutrition_str (str): A string that contains a list-like structure.
        with nutritional information.
        The expected format of the string is similar to:
        "[calories, total_fat, sugar, sodium, protein, saturated_fat, carbohydrates]".
        Example: "[250.0, 10.0, 12.0, 20.00, 5.0, 3.0, 30.0]"

    Returns:
        list: A list of 7 nutritional values as floats, or a list of 7 `None` elements
        if the string could not be parsed. The 7 elements correspond to:
            - Calories (Kcal) (float)
            - Total Fat (%day) (float)
            - Sugar (%day) (float)
            - Sodium (%day) (float)
            - Protein (%day) (float)
            - Saturated Fat (%day) (float)
            - Carbohydrates (%day) (float)

    Example:
        >>> parse_nutrition("[250.0, 10.0, 12.0, 20.00, 5.0, 3.0, 30.0]")
        [250.0, 10.0, 12.0, 20.00, 5.0, 3.0, 30.0]

        >>> parse_nutrition("invalid_string")
        [None, None, None, None, None, None, None]

    Raises:
        None: This function does not raise exceptions but instead catches parsing errors
        and returns a list of `None` values if the input is not in the correct format.
    """
    try:
        # Attempt to parse the string into a Python list using literal_eval
        return ast.literal_eval(nutrition_str)
    except (ValueError, SyntaxError):
        # Return a list of 7 None elements if there's a parsing error
        return [None] * 7


def stats_bio(df_preprocessed: pd.DataFrame) -> pd.DataFrame:
    """
    This function processes a filtered DataFrame of bio recipes and performs.
    the following tasks:
    1. Extracts and parses the 'nutrition' column to convert stringified.
    nutrition data into a usable format.
    2. Calculates statistical indicators (mean, median, etc.) for various.
      nutritional components.
    3. Adds ranking columns to the DataFrame for calories, fats,
        sugars, sodium, proteins.
      saturated fats, and carbohydrates.
    4. Identifies and flags the top 5 recipes in each nutritional component.
    based on the highest values.
    The resulting DataFrame contains the original recipe data.
    the parsed nutritional components.
    the ranking for each component, and boolean flags indicating whether.
    a recipe is in the top 5 for each category.
    Args:
        df_filtered_bio (pd.DataFrame): A filtered DataFrame containing recipe data.
        The DataFrame must include
        a column 'nutrition', where the nutritional information for each recipe.
        is stored as a string.
    Returns
        pd.DataFrame: A DataFrame containing the original recipe data,
        parsed nutritional data, rankings for each nutritional component,
        and boolean flags for top 5 recipes in each category.
    Example:
        # Assuming df_filtered_bio is a DataFrame with a 'nutrition' column.
        # in string format.
        combined_df = stats_bio(df_filtered_bio)
        combined_df.head()  # To see the result
    """
    # Apply the parse_nutrition function to the 'nutrition' column
    nutrition_data = df_preprocessed["nutrition"].dropna().apply(parse_nutrition)
    # Keep only rows where the parsed data has exactly 7 elements
    nutrition_data = nutrition_data[nutrition_data.apply(lambda x: len(x) == 7)]
    # current daily values found in
    # https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels
    current_daily_total_fat = 78
    current_daily_total_sugar = 50
    current_daily_total_sodium = 2300
    current_daily_total_protein = 50
    current_daily_total_saturated_fat = 20
    current_daily_total_carbo = 275
    # Convert the list of nutrition data into a DataFrame with appropriate column names
    nutrition_df = pd.DataFrame(
        nutrition_data.tolist(),
        columns=[
            "Calories",
            "Total Fat (g)",
            "Sugar (g)",
            "Sodium (mg)",
            "Protein (g)",
            "Saturated Fat (g)",
            "Carbohydrates (g)",
        ],
    )
    # convert %daily value to interational measures(g,mg)
    nutrition_df["Total Fat (g)"] = (
        (nutrition_df["Total Fat (g)"] * current_daily_total_fat)
    ) / 100
    nutrition_df["Sugar (g)"] = (
        (nutrition_df["Sugar (g)"] * current_daily_total_sugar)
    ) / 100
    nutrition_df["Sodium (mg)"] = (
        (nutrition_df["Sodium (mg)"] * current_daily_total_sodium)
    ) / 100
    nutrition_df["Protein (g)"] = (
        (nutrition_df["Protein (g)"] * current_daily_total_protein)
    ) / 100
    nutrition_df["Saturated Fat (g)"] = (
        (nutrition_df["Saturated Fat (g)"] * current_daily_total_saturated_fat)
    ) / 100
    nutrition_df["Carbohydrates (g)"] = (
        (nutrition_df["Carbohydrates (g)"] * current_daily_total_carbo)
    ) / 100
    # Calculate basic statistical indicators: mean, median, standard deviation, min, max
    combined_df = pd.concat(
        [df_preprocessed.reset_index(drop=True), nutrition_df], axis=1
    )
    # filter values of combined_df by putting values higher than 1
    combined_df = combined_df[combined_df["Calories"] > 1]
    combined_df = combined_df[combined_df["Total Fat (g)"] > 1]
    combined_df = combined_df[combined_df["Sugar (g)"] > 1]
    combined_df = combined_df[combined_df["Sodium (mg)"] > 1]
    combined_df = combined_df[combined_df["Saturated Fat (g)"] > 1]
    combined_df = combined_df[combined_df["Protein (g)"] > 1]
    combined_df = combined_df[combined_df["Carbohydrates (g)"] > 1]
    # Sort each nutritional component in ascending order to get the lowest values
    # Flag the top 4 for each nutrient by sorting and selecting the first 4 rows
    # Get the indices of the top 4 for each nutritional component
    # maximizing the protein ranking but minimizing the others
    top_4_calories = combined_df["Calories"].nsmallest(4).index
    top_4_fat = combined_df["Total Fat (g)"].nsmallest(4).index
    top_4_sugar = combined_df["Sugar (g)"].nsmallest(4).index
    top_4_sodium = combined_df["Sodium (mg)"].nsmallest(4).index
    top_4_saturated_fat = combined_df["Saturated Fat (g)"].nsmallest(4).index
    top_4_carbohydrates = combined_df["Carbohydrates (g)"].nsmallest(4).index
    top_4_protein = combined_df["Protein (g)"].nlargest(4).index

    # Flag the top 4 for each nutritional component
    # Using vectorized operations (boolean column value)
    combined_df["Top 4 Calories"] = combined_df.index.isin(top_4_calories)
    combined_df["Top 4 Total Fat"] = combined_df.index.isin(top_4_fat)
    combined_df["Top 4 Sugar"] = combined_df.index.isin(top_4_sugar)
    combined_df["Top 4 Sodium"] = combined_df.index.isin(top_4_sodium)
    combined_df["Top 4 Saturated Fat"] = combined_df.index.isin(top_4_saturated_fat)
    combined_df["Top 4 Carbohydrates"] = combined_df.index.isin(top_4_carbohydrates)
    combined_df["Top 4 Protein"] = combined_df.index.isin(top_4_protein)
    return combined_df


combined_df = stats_bio(df_preprocessed)
print(combined_df)
