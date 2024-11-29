import plotly.express as px

from data_loader import DataLoader

# Loads the raw interactions dataset using the data_loader module
data_loader = DataLoader()
interactions_preprocessed = data_loader.load_data(
    "preprocessed_data/PP_interactions_mangetamain.csv"
)
# Creates a histogram to show the dynamics of interactions over time
fig2 = px.histogram(interactions_preprocessed.date)
print(fig2)
fig2.add_annotation(
    text="Instagram",
    x="2012-01-31",  # x position in the time interval (adjust as needed)
    y=6000,  # y position (adjust as needed)
    showarrow=False,
    font=dict(size=15, color="green"),
    bgcolor="rgba(255, 255, 255, 0.7)",  # Semi-transparent white background
    bordercolor="black",
    borderwidth=3,
    borderpad=4,
)

# Updates the labels of the axes
fig2.update_layout(
    xaxis_title="Time",  # x-axis label
    yaxis_title="Number of interactions",  # y-axis label
    showlegend=True,  # Enable the legend
    title=dict(
        text="Evolution of interactions",  # Graph title
        x=0.5,  # Center the title
        xanchor="center",
        yanchor="top",
        font=dict(size=20),  # Font size
    ),
)
