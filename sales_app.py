# dash app to display the sales data

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# read the sales data
df = pd.read_csv('data/pink_morsel_sales.csv')

# convert sales to numeric (remove $ sign)
df['sales'] = df['sales'].str.replace('$', '').astype(float)

# convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# create the dash app
app = dash.Dash(__name__)

# create the layout
app.layout = html.Div([
    html.H1('Pink Morsel Sales', style={'textAlign': 'center', 'marginBottom': 30}),
    
    # Region filter
    html.Div([
        html.Label('Select Region:', style={'marginRight': 10}),
        dcc.Dropdown(
            id='region-filter',
            options=[
                {'label': 'All Regions', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'South', 'value': 'south'},
                {'label': 'East', 'value': 'east'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            style={'width': '200px', 'display': 'inline-block'}
        )
    ], style={'marginBottom': 20, 'marginLeft': 20}),
    
    # Sales graph
    dcc.Graph(id='sales-graph'),
    
    # Summary statistics
    html.Div(id='summary-stats', style={'marginTop': 20, 'marginLeft': 20})
])

# callback to update graph based on region filter
@app.callback(
    [Output('sales-graph', 'figure'),
     Output('summary-stats', 'children')],
    [Input('region-filter', 'value')]
)
def update_graph(selected_region):
    # filter data by region
    if selected_region == 'all':
        # sum sales across all regions by date
        filtered_df = df.groupby('date')['sales'].sum().reset_index()
        # create single line chart for total sales
        fig = px.line(
            filtered_df,
            x='date',
            y='sales',
            title='Total Sales Over Time (All Regions Combined)',
            labels={'sales': 'Sales ($)', 'date': 'Date'}
        )
    else:
        filtered_df = df[df['region'] == selected_region]
        # create line chart showing sales over time for selected region
        fig = px.line(
            filtered_df,
            x='date',
            y='sales',
            title=f'Sales Over Time - {selected_region.capitalize()}',
            labels={'sales': 'Sales ($)', 'date': 'Date'}
        )
    
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        hovermode='x unified'
    )
    
    # calculate summary statistics
    total_sales = filtered_df['sales'].sum()
    avg_sales = filtered_df['sales'].mean()
    max_sales = filtered_df['sales'].max()
    
    stats = html.Div([
        html.H3('Summary Statistics'),
        html.P(f'Total Sales: ${total_sales:,.2f}'),
        html.P(f'Average Daily Sales: ${avg_sales:,.2f}'),
        html.P(f'Maximum Daily Sales: ${max_sales:,.2f}')
    ])
    
    return fig, stats

# run the app
if __name__ == '__main__':
    app.run(debug=True)