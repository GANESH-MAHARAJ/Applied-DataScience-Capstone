import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown to select the launch site
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    
    html.Br(),
    
    # Pie chart for successful vs failed launches
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # Range slider for selecting payload mass
    dcc.RangeSlider(
        id='payload-slider',
        min=spacex_df['Payload Mass (kg)'].min(),
        max=spacex_df['Payload Mass (kg)'].max(),
        step=1000,
        marks={i: str(i) for i in range(int(spacex_df['Payload Mass (kg)'].min()), int(spacex_df['Payload Mass (kg)'].max()) + 1, 5000)},
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()],
        className="range-slider"  # Apply custom CSS class
    ),

    # Scatter plot for success vs payload
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2: Add a callback to update the success-pie-chart based on the selected site
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # If 'ALL' is selected, create a pie chart for all launch sites
        pie_chart = px.pie(spacex_df, names='Launch Site', 
                           color='Launch Site',  # Different color for each site
                           title='Success vs. Failure Launches (All Sites)',
                           hole=0.3)  # Adding a hole to make it a donut chart
        pie_chart.update_traces(textinfo='percent+label')  # Show percentage and label
    else:
        # If a specific site is selected, filter the data for that site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        pie_chart = px.pie(filtered_df, names='class',
                           title=f'Success vs. Failure Launches ({selected_site})',
                           hole=0.3)  # Adding a hole to make it a donut chart
        pie_chart.update_traces(textinfo='percent')  # Show only percentage, not class label
    
    return pie_chart

# TASK 4: Add a callback to update the success-payload-scatter-chart based on selected payload range
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        
    # Create the scatter plot
    scatter_chart = px.scatter(
        filtered_df, x='Payload Mass (kg)', y='class', color='Launch Site',
        title=f'Success vs Payload Mass ({selected_site})'
    )
    return scatter_chart

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
