import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5, 6],
    'y': [1, 4, 9, 16, 25, 36],
    'category': ['A', 'A', 'B', 'B', 'C', 'C'],
    'subcategory': ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']
})

# Create an initial scatter plot with Plotly Express
fig = px.scatter(df, x='x', y='y', color='category', symbol='sub_category')

# Symbol list (extend as needed)
symbols = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 'triangle-left', 'triangle-right']

# Update symbols in the layout
for i, trace in enumerate(fig['data']):
    trace['marker']['symbol'] = symbols[i % len(symbols)]

fig.show()
