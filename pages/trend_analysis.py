import requests
import dash
import pandas as pd
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import io
import base64
from wordcloud import WordCloud

load_figure_template('LUX')

external_stylesheets = [dbc.themes.LUX]
dash.register_page(__name__, external_stylesheets=external_stylesheets)

layout = html.Div([
    html.Div([html.H1("Twitter Trend Analysis")], style={"text-align":"center", "margin-top":"10px"}),
    dbc.Row([
        dbc.Col(html.Label('Select Country:'), width=3, style={'margin-right': '0px', 'margin-left':'40px'}),
        dbc.Col(html.Label('Select City:'), width=3, style={'margin-right': '0px', 'margin-left':'0px'})
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-1',
                options=[
                    {'label': 'Singapore', 'value':'Singapore'},
            {'label': 'United Arab Emirates', 'value':'United Arab Emirates'},
            {'label': 'Algeria', 'value':'Algeria'},
            {'label': 'Argentina', 'value':'Argentina'},
            {'label': 'Australia', 'value':'Australia'},
            {'label': 'Austria', 'value':'Austria'},
            {'label': 'Bahrain', 'value':'Bahrain'},
            {'label': 'Belgium', 'value':'Belgium'},
            {'label': 'Belarus', 'value':'Belarus'},
            {'label': 'Brazil', 'value':'Brazil'},
            {'label': 'Canada', 'value':'Canada'},
            {'label': 'Chile', 'value':'Chile'},
            {'label': 'Colombia', 'value':'Colombia'},
            {'label': 'Denmark', 'value':'Denmark'},
            {'label': 'Dominican Republic', 'value':'Dominican Republic'},
            {'label': 'Ecuador', 'value':'Ecuador'},
            {'label': 'Egypt', 'value':'Egypt'},
            {'label': 'Ireland', 'value':'Ireland'},
            {'label': 'France', 'value':'France'},
            {'label': 'Ghana', 'value':'Ghana'},
            {'label': 'Germany', 'value':'Germany'},
            {'label': 'Greece', 'value':'Greece'},
            {'label': 'Guatemala', 'value':'Guatemala'},
            {'label': 'Indonesia', 'value':'Indonesia'},
            {'label': 'India', 'value':'India'},
            {'label': 'Israel', 'value':'Israel'},
            {'label': 'Italy', 'value':'Italy'},
            {'label': 'Japan', 'value':'Japan'},
            {'label': 'Jordan', 'value':'Jordan'},
            {'label': 'Kenya', 'value':'Kenya'},
            {'label': 'Korea', 'value':'Korea'},
            {'label': 'Kuwait', 'value':'Kuwait'},
            {'label': 'Lebanon', 'value':'Lebanon'},
            {'label': 'Latvia', 'value':'Latvia'},
            {'label': 'Oman', 'value':'Oman'},
            {'label': 'Mexico', 'value':'Mexico'},
            {'label': 'Malaysia', 'value':'Malaysia'},
            {'label': 'Nigeria', 'value':'Nigeria'},
            {'label': 'Netherlands', 'value':'Netherlands'},
            {'label': 'Norway', 'value':'Norway'},
            {'label': 'New Zealand', 'value':'New Zealand'},
            {'label': 'Peru', 'value':'Peru'},
            {'label': 'Pakistan', 'value':'Pakistan'},
            {'label': 'Poland', 'value':'Poland'},
            {'label': 'Panama', 'value':'Panama'},
            {'label': 'Portugal', 'value':'Portugal'},
            {'label': 'Qatar', 'value':'Qatar'},
            {'label': 'Philippines', 'value':'Philippines'},
            {'label': 'Puerto Rico', 'value':'Puerto Rico'},
            {'label': 'Russia', 'value':'Russia'},
            {'label': 'Saudi Arabia', 'value':'Saudi Arabia'},
            {'label': 'South Africa', 'value':'South Africa'},
            {'label': 'Spain', 'value':'Spain'},
            {'label': 'Sweden', 'value':'Sweden'},
            {'label': 'Switzerland', 'value':'Switzerland'},
            {'label': 'Thailand', 'value':'Thailand'},
            {'label': 'Turkey', 'value':'Turkey'},
            {'label': 'United Kingdom', 'value':'United Kingdom'},
            {'label': 'Ukraine', 'value':'Ukraine'},
            {'label': 'United States', 'value':'United States'},
            {'label': 'Venezuela', 'value':'Venezuela'},
            {'label': 'Vietnam', 'value':'Vietnam'}
        ], value='India',
                style={'width': '100%', 'margin-right': '20px', 'margin-left':'20px'}
            ),
            width=3
        ),
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-2',
                style={'width': '100%', 'margin-right': '20px', 'margin-left':'20px'}
            ),
            width=3
        )
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Most Trending Topics", style={"margin-left": "40px", "margin-top":"10px"})
        ]),
        dbc.Col([
            html.H2("Word Cloud Analysis of Trending Topics", style={"margin-top":"10px"})
        ])
    ]),
    dbc.Row([
            dbc.Col([
                html.Div(id='table-container', children="")
            ], style={"maxHeight": "650px", "maxWidth": "915px", "overflow": "auto", "margin-left": '30px',
                  "margin-top": '5px'}),
            dbc.Col([
                html.Div([
                    html.Img(id='wordcloud-img'),
                    dcc.Graph(id='bar-plot')
                ], style={"maxHeight": "600px","margin-top": "5px", "margin-left": '10px'})
            ], width=6)
    ])
])


@callback(
    Output('dropdown-2', 'options'),
    [Input('dropdown-1', 'value')]
)

def update_dropdown_2(selected_value):
    url = "https://twitter154.p.rapidapi.com/trends/available"

    headers = {
	    'X-RapidAPI-Key': 'b562866153msh5e1d941a3df3ccap1b44c7jsn26513444237b',
	    "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers)
    code = response.json()
    woeid_of_cities = []
    for c in code:
        if c['country']==selected_value:
            woeid_of_cities.append({'label':str(c['name']), 'value':str(c['woeid'])})
    
    return woeid_of_cities
    
@callback(
    [Output('table-container', 'children'),
     Output('wordcloud-img', 'src'),
     Output('bar-plot', 'figure')],
    [Input('dropdown-2', 'value')]
)

def update_table(selected_woeid):
    if selected_woeid:
        url = "https://twitter154.p.rapidapi.com/trends/"

        querystring = {"woeid":str(selected_woeid)}

        headers = {
            'X-RapidAPI-Key': 'b562866153msh5e1d941a3df3ccap1b44c7jsn26513444237b',
            "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        trends_df = pd.DataFrame(response.json()[0]['trends'])
        
        trends_df.drop(["promoted_content", "query"], axis=1, inplace=True)
        
        trends_df.rename(columns={"name":"TRENDING TOPICS", "url":"URL", "tweet_volume":"TWEET VOLUME"}, inplace=True)

        table = dbc.Table.from_dataframe(trends_df, striped=True, bordered=True, hover=True)
        
        wordcloud = WordCloud(width=700, height=300, background_color='white').generate_from_frequencies(
            {name: number for name, number in zip(trends_df['TRENDING TOPICS'], trends_df['TWEET VOLUME']) if pd.notnull(number)})

        img_data = io.BytesIO()
        wordcloud.to_image().save(img_data, format='PNG')
        img_data.seek(0)
        img_base64 = base64.b64encode(img_data.getvalue()).decode()
        
        trends_df = trends_df.dropna(subset=["TWEET VOLUME"])
        top_10_names = trends_df.sort_values(by='TWEET VOLUME', ascending=True)[len(trends_df)-10:]
        
        bar_plot = go.Figure(go.Bar(
            x=top_10_names['TWEET VOLUME'],
            y=top_10_names['TRENDING TOPICS'],
            orientation='h'
        ))
        bar_plot.update_layout(title={
            'text': 'Top 10 Trending Topics',
            'x': 0.5,  
            'xanchor': 'center',  
            'font': {'size': 25}
        }, xaxis_title='TWEET VOLUME', yaxis_title='TOPICS')

        return table, 'data:image/png;base64,' + img_base64, bar_plot

