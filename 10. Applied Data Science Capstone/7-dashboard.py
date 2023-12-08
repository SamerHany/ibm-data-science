# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
site_list = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    # HEADER
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'margin': '0px',
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40,
            'padding': '20px',
            'border-radius': '20px',
            'background': '#fafafa',
            'box-shadow':  '0px 20px 60px #bebebe, -20px -20px 60px #ffffff',
        }
    ),

    # PIE CHART
    html.Div([
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        html.P("Launch Site:", style={'font-weight': 'bold'}),
        dcc.Dropdown(id='site-dropdown', options=site_list, value='ALL', placeholder='Select a Launch Site here', searchable=True),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart'), style={'margin-top': '30px'}),
    ], style={
        'margin-top': '30px',
        'padding': '20px',
        'border-radius': '20px',
        'background': '#fafafa',
        'box-shadow':  '0px 20px 60px #bebebe, -20px -20px 60px #ffffff',
    }),


    # SCATTER CHART
    html.Div([
        html.P("Payload range (Kg):", style={'font-weight': 'bold'}),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload]),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart'), style={'margin-top': '30px'}),
    ], style={
        'margin-top': '30px',
        'padding': '20px',
        'border-radius': '20px',
        'background': '#fafafa',
        'box-shadow':  '0px 20px 60px #bebebe, -20px -20px 60px #ffffff',
    }),
], style={
    'font-family': 'Arial',
    'padding': '30px 10%'
})

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'), 
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title='Total Success Launches for Site {}'.format(selected_site))

    fig.update_layout({
        'plot_bgcolor':'#fafafa',
        'paper_bgcolor':'#fafafa',
    })

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'), 
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation Between Payload and Success for All Sites')
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation Between Payload and Success for Site {}'.format(selected_site))

    fig.update_layout({
        'plot_bgcolor':'#fafafa',
        'paper_bgcolor':'#fafafa',
        'xaxis': {'gridcolor': '#d3d3d3', 'zerolinecolor': '#d3d3d3', 'tickmode': 'linear', 'dtick': 1000},
        'yaxis': {'gridcolor': '#d3d3d3', 'zerolinecolor': '#d3d3d3', 'tickmode': 'array', 'tickvals': [0, 1], 'ticktext': ['(Failure) 0', '(Success) 1']},
    })

    return fig



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)