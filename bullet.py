import plotly.graph_objects as go

data = [{'red': [20, 25]}, {'green': [25, 22]}, {'blue': [18, 13]}]

fig = go.Figure()

# Add vertical bar chart trace
for i in range(len(data)):
    key, values = list(data[i].items())[0]
    fig.add_trace(go.Bar(
        x=[key],
        y=[values[0]],
        name=key,
        marker_color='rgba(50, 171, 96, 0.5)',
        width=0.5,
        orientation='v'
    ))

# Add horizontal line marker trace
for i in range(len(data)):
    key, values = list(data[i].items())[0]
    fig.add_trace(go.Scatter(
        x=[key],
        y=[values[1]],
        mode='markers',
        marker_symbol='141',
        marker_color='red',
        marker_size=180,
        marker_line_width=6,
        name=key,
        # line=dict(color='black', width=4),
        showlegend=False,
    ))

# Update layout
fig.update_layout(
    title='Bullet Chart',
    yaxis=dict(
        title='Value',
        range=[0, 30],
    ),
    xaxis=dict(
        title='Category',
    ),
    barmode='stack',
    bargap=0.1,
    bargroupgap=0.1,
)

# Show figure
fig.show()
