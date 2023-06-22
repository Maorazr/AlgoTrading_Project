from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True
           )
server = app.server
app.layout = html.Div([
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} ", href=page["relative_path"],
                    style={'color': 'black', 'font-family': 'Arial',
                           'margin': '10px', 'font-size': '16px'}
                )
            )
            for page in dash.page_registry.values()
        ],
        style={'display': 'flex', 'flex-direction': 'row'}
    ),

    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
