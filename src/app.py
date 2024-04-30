import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv('dataseta.csv')

# Create a Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout
app.layout = html.Div([
    html.H1("Advertisement Analysis"),
    dcc.Dropdown(
        id='industry-dropdown',
        options=[{'label': industry, 'value': industry} for industry in df['Industry'].unique()],
        placeholder='Select Industry'
    ),
    dcc.Dropdown(
        id='magna-category-dropdown',
        placeholder='Select Magna Category'
    ),
    dcc.Dropdown(
        id='pub-genre-dropdown',
        placeholder='Select Pub Genre'
    ),
    dcc.Dropdown(
        id='publication-dropdown',
        placeholder='Select Publication'
    ),
    dcc.Graph(id='top-10-lowest-graph'),
    dcc.Graph(id='top-10-highest-graph'),


    html.Hr(),
    html.H1("Advertisement Analysis"),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='publication-dropdown',
                options=[{'label': publication, 'value': publication} for publication in df['Publication'].unique()],
                placeholder='Select Publication'
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='top-10-lowest-graph'),
            dcc.Graph(id='top-10-highest-graph')
        ], style={'width': '70%', 'display': 'inline-block'})
    ]),
    html.Div([
        dcc.Graph(id='industry-count-graph')
    ])


])

# Define callback to update Magna Category dropdown based on Industry selection
@app.callback(
    Output('magna-category-dropdown', 'options'),
    [Input('industry-dropdown', 'value')]
)
def update_magna_category_dropdown(selected_industry):
    if selected_industry is None:
        return []
    options = [{'label': magna_category, 'value': magna_category} for magna_category in df[df['Industry'] == selected_industry]['Magna Category'].unique()]
    return options

# Define callback to update Pub Genre dropdown based on Magna Category selection
@app.callback(
    Output('pub-genre-dropdown', 'options'),
    [Input('magna-category-dropdown', 'value')]
)
def update_pub_genre_dropdown(selected_magna_category):
    if selected_magna_category is None:
        return []
    options = [{'label': pub_genre, 'value': pub_genre} for pub_genre in df[df['Magna Category'] == selected_magna_category]['Pub Genre'].unique()]
    return options

# Define callback to update Publication dropdown based on Pub Genre selection
@app.callback(
    Output('publication-dropdown', 'options'),
    [Input('pub-genre-dropdown', 'value')]
)
def update_publication_dropdown(selected_pub_genre):
    if selected_pub_genre is None:
        return []
    options = [{'label': publication, 'value': publication} for publication in df[df['Pub Genre'] == selected_pub_genre]['Publication'].unique()]
    return options

# Define callback to update top 10 lowest and highest advertiser graphs based on Pub Genre selection
@app.callback(
    [Output('top-10-lowest-graph', 'figure'),
     Output('top-10-highest-graph', 'figure')],
    [Input('pub-genre-dropdown', 'value')]
)
def update_graphs(selected_pub_genre):
    if selected_pub_genre is None:
        return {}, {}

    # Filter data based on selected Pub Genre
    filtered_df = df[df['Pub Genre'] == selected_pub_genre]

    # Calculate top 10 lowest and highest advertisers
    top_10_lowest = filtered_df.groupby('Advertiser')['Spends'].sum().nsmallest(10).reset_index()
    top_10_highest = filtered_df.groupby('Advertiser')['Spends'].sum().nlargest(10).reset_index()

    # Create bar graphs
    fig_lowest = px.bar(top_10_lowest, x='Spends', y='Advertiser', orientation='h', title='Top 10 Lowest Advertisers')
    fig_highest = px.bar(top_10_highest, x='Spends', y='Advertiser', orientation='h', title='Top 10 Highest Advertisers')

    return fig_lowest, fig_highest






if __name__ == '__main__':
    app.run_server(debug=True, port=8952)
