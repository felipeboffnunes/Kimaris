import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

search_string_input = dbc.FormGroup(
    [
        dbc.Label("Search String", html_for="search-string-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="search-string-row", placeholder="Enter title"
            ),
            width=10,
        ),
    ],
    row=True,
)

date_input = dbc.FormGroup(
    [
        dbc.Label("Date", html_for="date-row", width=2),
        dbc.Col(
            dcc.DatePickerRange(
                id="date-row",
                display_format="Y"
            ),
            width=10,
        ),
    ],
    row=True,
)


databases_input = dbc.FormGroup(
    [
        dbc.Label("Databases", html_for="databases-row", width=2),
        dbc.Col(
            dbc.Checklist(
                id="databases-row",
                options=[
                    {"label": "Google Scholar", "value": 1},
                    
                    {
                        "label": "ACM Library", 
                        "value": 2,
                        "disabled": True,
                    },
                    
                    {
                        "label": "Elsevier",
                        "value": 3,
                        "disabled": True,
                    },
                ],
            ),
            width=10,
        ),
    ],
    row=True,
)

review_form = dbc.Form([search_string_input, date_input, databases_input], style={"width": "100%"})