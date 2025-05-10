from dash import Dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from layout import layout
from utils import update_output, save_file

app = Dash(
    __name__,
    external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
        dbc.themes.BOOTSTRAP,
    ],
)
server = app.server
app.layout = layout


@app.callback(Output("mask-save-index", "data"), Input("mask-save", "n_clicks"))
def stub_save_file(n_clicks):
    return save_file(n_clicks)

@app.callback(
    Output("output-image-upload", "children"),
    Output("mask-image-upload", "children"),
    Output("graph", "children"),
    Input("upload-image", "contents"),
    State("dropdown", "value"),
)
def stub_update_output(list_of_contents, server_type):
    return update_output(list_of_contents, server_type)

if __name__ == "__main__":
    app.run_server(debug=True)
