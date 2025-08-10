import plotly.graph_objects as go

# Data
stages = ['Website Visit', 'Downloads', 'Leads', 'Opportunities', 'Sales']
values = [1000, 500, 200, 100, 50]

# Create the funnel chart
fig = go.Figure(go.Funnel(
    y=stages,
    x=values,
    textposition="inside",
    textinfo="value+percent initial+percent previous",
    opacity=0.8,
    connector={"line": {"color": "royalblue", "dash": "dot", "width": 3}},
    marker={"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"]},
))

# Update layout
fig.update_layout(
    title={
        "text": "Sales Funnel",
        "x": 0.5,
        "xanchor": "center",
        "font": {"size": 24}
    },
    font=dict(
        family="Arial",
        size=14
    ),
    width=900,
    height=700,
    paper_bgcolor="LightSteelBlue",
)

# Show the plot
fig.show()