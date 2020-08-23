# Python Standard Libraries

# External Libraries
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Reset graph", id="reset-graph-button", n_clicks=0),
            id="reset-graph-col", 
            width="auto"
        ),
        dbc.Col(
            dbc.Button("Open graph", id="open-graph-button", n_clicks=0),
            id="open-graph-col", 
            width="auto"
        ),   
        dbc.Col(
            dbc.NavLink(dbc.Button("Select node", id="select-node-button", n_clicks=0),
            href="/article",
            id="node-link"
            ),
            id="select-node-col", 
            width="auto"
        ),
        dbc.Col(
            dbc.NavLink(dbc.Button("Select article", id="select-article-button", n_clicks=0),
            href="/article",
            id="article-link"
            ),
            id="select-article-col", 
            width="auto"
        ),
    ],
    no_gutters=True,
    className="flex-nowrap mt-3 mt-md-3",
    align="center",

)

help_items = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Info", id="info-open-button", n_clicks=0),
            id="info-open-col", 
            width="auto"
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Instructions"),
                dbc.ModalBody(
                    dcc.Tabs([
                        dcc.Tab([
                            html.Div([
                                html.P("Avoid clicking in a node whilst trying to move the graph, or you will open the node. Click on empty spaces or lines while rotating or moving the graph."),
                                html.Img(src="./assets/graph3d.gif", style={"max-width": "70%", "height": "auto", "margin-left": "auto", "margin-right": "auto", "display": "block"}),  
                                html.Br(),  
                                html.P("Red circles inside a node mean it is the one citing the others.\n \
                                To understand it better, if a node is central and it has a red circle, it means it is citing only the nodes that do not have a red circle.\n \
                                If a node is a leaf and has a red circle, it is citing the central node.")
                            ])
                        ], label="Graph"),
                        dcc.Tab([
                            html.Div([
                                html.Br(),
                                html.P("Reset Graph - Opens graph with all the nodes from the review."),
                                html.P("Open Graph - If a cell table is selected on the articles table, it opens the graph of the connections of that article."),
                                html.P("Select Node - If a node has been selected in the graph, opens the article page of that node."),
                                html.P("Select Article - If a cell table has been selected in the articles table, opens the article page of that cell."),
                                html.Br()
                            ])
                        ], label="Buttons")
                    ])
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="info-close-button", className="ml-auto")
                ),
            ],
            id="info-modal",
        ),
    ],
    style={"right": "0", "position": "absolute"}
)
BOTTOM_MENU = dbc.Navbar(
    [
        menu_items,
        help_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="bottom_menu")