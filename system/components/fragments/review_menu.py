# External Libraries
import dash_bootstrap_components as dbc

review_menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.NavLink(dbc.Button("Go back", id="return-review-button", n_clicks=0),
            href="/page-3",
            id="page-3-link"
            ),
            id="return-review-col", 
            width="auto"
        ),
        dbc.Col(
            dbc.Button("Search", id="search-button", n_clicks=0),
            id="search-col", 
            width="auto"
        ),
    ],
    no_gutters=True,
    className="flex-nowrap mt-3 mt-md-3",
    align="center",

)
REVIEW_MENU = dbc.Navbar(
    [
        review_menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="review-menu")
