# External Libraries
import dash_core_components as dcc
import dash_html_components as html
# Fragments
from components.fragments.review_form import review_form
from components.fragments.review_menu import REVIEW_MENU


reviews_page = html.Div([
                html.Div([
                    review_form, 
                    REVIEW_MENU
                ], id="research", style={"padding": "2em"})
            ])