import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dcc.Location(id='url', refresh=False),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("X Analysis Dashboard", className="header-title"),
                    ],
                    width=10,
                )
            ],
            style={'padding-top': '20px', 'padding-bottom': '10px', 'border-bottom': '1px solid #c8c8c8', 'background-color': '#f8f9fa'}
        ),
        dbc.Row(
            [
                dbc.Col(
                [
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink(f"{page['name']}", href=page["relative_path"], active=False, className="nav-link")
                            )
                            for page in dash.page_registry.values() if page["relative_path"] != "/"
                        ],
                        pills=True,
                        className="flex-column"                        
                    )
                ],
                width=2,        
                style={'padding-top': '20px', 'border-right': '1px solid #c8c8c8', 'height': '100vh', 'background-color': '#f8f9fa'}
                ),
                dbc.Col(
                    dash.page_container 
                )
            ]
        )
    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=False)
