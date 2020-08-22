# Python Standard Libraries

# External Libraries
import dash_bootstrap_components as dbc

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
BOTTOM_MENU = dbc.Navbar(
    [
        menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="bottom_menu")