import plotly.express as px

from data_loader import DataLoader

# Loads the raw interactions dataset using the data_loader module
data_loader = DataLoader()
interactions_preprocessed = data_loader.load_data(
    "preprocessed_data/PP_interactions_mangetamain.csv"
)
# Creates a histogram to show the dynamics of interactions over time
fig2 = px.histogram(interactions_preprocessed.date, color_discrete_sequence=["green"])
# Add an annotation for the interaction drop with hover info
# Add an annotation for the interaction drop with hover info
fig2.add_annotation(
    x="2011-01-01",  # Adjust the date as needed
    y=4500,  # Adjust y based on your data
    text="🔻",  # Emoji to make it visible, you can use other small characters
    showarrow=True,
    arrowhead=3,
    arrowcolor="pink",
    ax=0,  # Adjust horizontal offset for the arrowhead
    ay=-100,  # Adjust vertical offset
    hovertext=(
        "🌟 The website was highly visited before 2011. "
        "Instagram's rise impacted visitor numbers after 2011."
    ),
    hoverlabel=dict(
        bgcolor="pink",  # Changed to a more noticeable color
        font_size=14,
        font_color="black",
    ),
)
# Update the layout
fig2.update_layout(
    xaxis_title="Time",  # x-axis label
    yaxis_title="Number of interactions",  # y-axis label
    title=dict(
        text="Evolution of Interactions Over Time",
        x=0.5,  # Center the title
        font=dict(size=20),
    ),
    hovermode="x unified",  # Unified hover across the x-axis
)
