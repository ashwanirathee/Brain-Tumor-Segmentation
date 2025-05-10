from dash import dcc, html
import dash_bootstrap_components as dbc

layout = html.Div(
    [
        dbc.Card(
            dbc.Row(
                [
                    dbc.Col([html.H1("Tumor Analysis Tooling")]),
                    dbc.Col(
                        [
                            html.P(
                                "Winning submission for MHacks21 which provides a tool to annotate brain tumor which is computer aided(the initial mask comes for radiologists).Automatic segmentation of brain tumors from medical images is important for clinical assessment and treatment planning of brain tumors. "
                            ),
                        ]
                    ),
                ]
            ),
            className="divHeader",
        ),
        dbc.Card(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="dropdown",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in [
                                                "GCP server",
                                                "Heroku Server",
                                                "Local Server",
                                            ]
                                        ],
                                        value="Local Server",
                                    )
                                ),
                                dbc.Col(
                                    [
                                        html.Button("Save Mask", id="mask-save"),
                                        dcc.Download(id="mask-save-index"),
                                    ]
                                ),
                                dbc.Col(
                                    html.Button(
                                        html.A(
                                            "Github",
                                            href="https://github.com/ashwanirathee/tumor-analysis",
                                            target="_blank",
                                        ),
                                        id="button5",
                                        style={"width": "100%"},
                                    )
                                ),
                                dbc.Col(
                                    html.Button(
                                        html.A(
                                            "Explainer Video",
                                            href="https://youtu.be/NqmgTwvg_Dw",
                                            target="_blank",
                                        ),
                                        id="button8",
                                        # color="danger",
                                        style={"color": "white", "width": "100%"},
                                    )
                                ),
                            ]
                        ),
                    ),
                    dbc.Col(
                        dcc.Upload(
                            id="upload-image",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select Files")]
                            ),
                            style={
                                "padding": "10px",
                                "width": "auto",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "height": "35px",
                            },
                            multiple=True,
                        ),
                    ),
                ]
            ),
            className="buttons",
            color="light",
        ),
        html.Div(
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Button("Image"),
                                    html.Div(
                                        id="output-image-upload",
                                        className="w h",
                                        style={"border": "1px solid #ccc"},
                                    ),
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.Button("Mask"),
                                    html.Div(
                                        id="mask-image-upload",
                                        className="w h",
                                        style={"border": "1px solid #ccc"},
                                    ),
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.Button("Graph"),
                                    html.Div(
                                        id="graph",
                                        className="w h",
                                        style={"border": "1px solid #ccc"},
                                    ),
                                ],
                                width=4,
                            ),
                        ],
                        className="g-0",
                    )
                ],
                className="div4",
                style={"flex": "1", "overflow": "auto"},
            ),
            style={"flex": "1", "display": "flex", "flexDirection": "column"},
        ),
    ],
    style={"height": "100vh", "display": "flex", "flexDirection": "column"},
)
