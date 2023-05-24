import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the input CSV file
df = pd.read_csv('batsman_bowler.csv')

# Create an empty dictionary to store the aggregated data
data = {}

# Aggregate the data for each batter and bowler combination
for _, row in df.iterrows():
    batter = row['batter']
    bowler = row['bowler']
    runs = row['batsman_run']
    frequency = row['frequency']
    if batter not in data:
        data[batter] = {}
    if bowler not in data[batter]:
        data[batter][bowler] = {'runs': 0, 'frequency': 0}
    data[batter][bowler]['runs'] += runs
    data[batter][bowler]['frequency'] += frequency

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div([
    html.H1('Batsman Performance Dashboard'),
    html.Label('Select a batter:'),
    dcc.Dropdown(
        id='batter-dropdown',
        options=[{'label': batter, 'value': batter} for batter in data.keys()],
        value=list(data.keys())[0]
    ),
    dcc.Graph(id='performance-graph')
])

# Define the callback function to update the graph based on the selected batter
@app.callback(
    Output('performance-graph', 'figure'),
    Input('batter-dropdown', 'value')
)
def update_graph(batter):
    batter_data = data[batter]
    df = pd.DataFrame.from_dict(batter_data, orient='index').reset_index()
    df.columns = ['bowler', 'runs', 'frequency']
    
    fig = px.scatter(df, x='runs', y='frequency', color='bowler',
                     hover_data=['bowler', 'runs', 'frequency'],
                     labels={'runs': 'Batsman Run', 'frequency': 'Frequency'})
    
    fig.update_layout(
        xaxis_title='Batsman Run',
        yaxis_title='Frequency',
        title=f'Batsman Performance against Different Bowlers - {batter}'
    )
    
    return fig

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
