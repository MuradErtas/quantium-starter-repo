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

# custom CSS styles
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Pink Morsel Sales Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                padding: 40px;
            }
            h1 {
                color: #2d3748;
                font-size: 2.5em;
                font-weight: 700;
                margin-bottom: 10px;
                text-align: center;
            }
            .subtitle {
                text-align: center;
                color: #718096;
                margin-bottom: 40px;
                font-size: 1.1em;
            }
            .filter-container {
                background: #f7fafc;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .filter-label {
                font-weight: 600;
                color: #2d3748;
                font-size: 1.1em;
            }
            .graph-container {
                background: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            .stats-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                margin-bottom: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                transition: transform 0.2s;
            }
            .stat-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            .stat-label {
                font-size: 0.9em;
                opacity: 0.9;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .stat-value {
                font-size: 2em;
                font-weight: 700;
            }
            .Select-control {
                border-radius: 6px !important;
                border: 2px solid #e2e8f0 !important;
            }
            .Select-control:hover {
                border-color: #667eea !important;
            }
            .is-focused .Select-control {
                border-color: #667eea !important;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# create the layout
app.layout = html.Div([
    html.Div([
        html.H1('Pink Morsel Sales Dashboard'),
        html.P('Interactive sales analytics and insights', className='subtitle'),
        
        # Region filter
        html.Div([
            html.Label('Select Region:', className='filter-label'),
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
                style={'width': '250px', 'minWidth': '200px'}
            )
        ], className='filter-container'),
        
        # Sales graph
        html.Div([
            dcc.Graph(id='sales-graph')
        ], className='graph-container'),
        
        # Summary statistics
        html.Div(id='summary-stats', className='stats-container')
    ], className='container')
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
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', size=12),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True
        ),
        title=dict(
            font=dict(size=20, color='#2d3748'),
            x=0.5,
            xanchor='center'
        ),
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='#667eea',
            font_size=12,
            font_family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            font_color='#2d3748',
        )
    )
    
    # update line color and style
    fig.update_traces(
        line=dict(width=2),
        marker=dict(size=4)
    )
    
    # calculate summary statistics
    total_sales = filtered_df['sales'].sum()
    avg_sales = filtered_df['sales'].mean()
    max_sales = filtered_df['sales'].max()
    
    # create styled stat cards
    stats = html.Div([
        html.Div([
            html.Div('Total Sales', className='stat-label'),
            html.Div(f'${total_sales:,.2f}', className='stat-value')
        ], className='stat-card'),
        html.Div([
            html.Div('Average Daily Sales', className='stat-label'),
            html.Div(f'${avg_sales:,.2f}', className='stat-value')
        ], className='stat-card'),
        html.Div([
            html.Div('Maximum Daily Sales', className='stat-label'),
            html.Div(f'${max_sales:,.2f}', className='stat-value')
        ], className='stat-card')
    ])
    
    return fig, stats

# run the app
if __name__ == '__main__':
    app.run(debug=True)