# External Libraries
import dash_core_components as dcc
import dash_html_components as html

# Data
from components.data.table import get_table
from components.data.graph import get_graph, get_figure

# Fragments
from components.fragments.bottom_menu import BOTTOM_MENU

# Graph
# ID: GRAPH = graph
FIGURE = get_figure(standard=False, author=True)
GRAPH = get_graph(FIGURE)


AUTHOR_FIGURE = get_figure(standard=False, author=True)
AUTHOR_GRAPH = get_graph(AUTHOR_FIGURE)


# Table
# ID: table
TABLE = get_table()


review_page = html.Div([
            html.Div([
                html.Div([
                    dcc.Tabs([
                        dcc.Tab(
                            html.Div([
                                GRAPH
                            ]),
                        label="Authors"
                        ),
                        dcc.Tab(
                            html.Div([
                                AUTHOR_GRAPH
                            ]),
                        label="Papers"
                        ),
                        dcc.Tab(
                            html.Div([
                                dcc.Tabs([
                                    dcc.Tab(
                                        html.Div(id="years-metadata-div"), label="Years"
                                    ),
                                    dcc.Tab(
                                        html.Div(id="cites-metadata-div"), label="Cites"
                                    )
                                ]),
                                html.Div(id="callback-metadata")
                            ]),
                        label="Metadata"
                        )
                    ]),
                ], style={"width": "35%", "float": "left"}, className="columns"),
                html.Div([
                    TABLE
                ], style={"width": "65%", "float": "right"}, className="columns", id="table-div"),
                
            ], className="row"),
                
            html.Div([
                BOTTOM_MENU
            ]),
        ])