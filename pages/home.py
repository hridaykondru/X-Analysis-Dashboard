import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H3('This is a multi-page dashboard application created using Dash for Python for visualizing X'),
    html.Div([
        html.P('There are two types of visualizations:'),
        html.Ul([
            html.Li('User Analysis - Given the X username, various visualizations related to the user are displayed in separate tabs'),
            html.Li('Trend Analysis - Given the country and city, the trending topics in the city have been visualized')
        ])
    ]),
    html.P('Please use the links in the left sidebar to start.')
])